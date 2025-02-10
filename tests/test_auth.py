# tests/test_auth.py

import pytest
from fastapi.testclient import TestClient
from starlette.responses import RedirectResponse
from app.main import app
from app.services.oauth import oauth
from app.crud import user as crud  # app/crud/user.py에 정의된 함수들을 사용

# 더미 사용자 객체 (CRUD 함수 모킹 시 사용)
class FakeUser:
    id = 1
    email = "test@example.com"
    name = "Test User"


@pytest.fixture
def client():
    """FastAPI TestClient를 생성합니다."""
    with TestClient(app) as c:
        yield c


def test_root_without_session(client):
    """
    로그인하지 않은 상태에서 루트("/") 엔드포인트 호출 시
    'Hello, please login.' 메시지가 반환되어야 합니다.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, please login."}


def test_login_endpoint(client, monkeypatch):
    """
    /auth/login 엔드포인트가 OAuth 로그인 플로우를 시작하며
    외부 인증 제공자로 리다이렉션(302)을 발생시키는지 확인합니다.
    """

    # oauth.google.authorize_redirect를 가짜 함수로 대체합니다.
    async def fake_authorize_redirect(request, redirect_uri):
        return RedirectResponse(url="/fake-auth", status_code=302)

    monkeypatch.setattr(oauth.google, "authorize_redirect", fake_authorize_redirect)

    response = client.get("/auth/login", follow_redirects=False)
    assert response.status_code == 302
    # 리다이렉트 URL이 fake URL이어야 함
    assert response.headers["location"] == "/fake-auth"


def simulate_auth_callback(monkeypatch):
    """
    /auth/callback 엔드포인트에서 실행되는 외부 OAuth 호출 및
    DB 연동 부분을 가짜 함수로 대체(mock)하여 성공적인 로그인 상황을 만듭니다.
    """

    # oauth.google.authorize_access_token: id_token 없이 fallback 로직으로 진행하도록 설정
    async def fake_authorize_access_token(request):
        return {"access_token": "fake_access_token", "token_type": "Bearer"}

    monkeypatch.setattr(oauth.google, "authorize_access_token", fake_authorize_access_token)

    # oauth.google.get: userinfo_endpoint 호출 결과를 가짜 응답으로 대체
    class FakeResponse:
        def json(self):
            return {"sub": "123", "email": "test@example.com", "name": "Test User"}

    async def fake_get(url, token):
        return FakeResponse()

    monkeypatch.setattr(oauth.google, "get", fake_get)

    # DB CRUD 함수들을 가짜 함수로 대체하여 더미 사용자 객체를 반환
    monkeypatch.setattr(crud, "get_user_by_google_id", lambda db, google_id: None)
    monkeypatch.setattr(crud, "create_user", lambda db, user_info: FakeUser())
    monkeypatch.setattr(crud, "update_user", lambda db, user, user_info: FakeUser())


def test_auth_callback_endpoint(client, monkeypatch):
    """
    /auth/callback 엔드포인트 호출 시,
    OAuth 콜백 처리가 성공적으로 동작하여 세션에 사용자 정보가 저장되고
    홈("/")으로 리다이렉션되는지 확인합니다.
    """
    # OAuth와 DB 관련 함수들을 모킹
    simulate_auth_callback(monkeypatch)

    # /auth/callback 호출 (쿼리 파라미터 state와 code는 더미 값)
    response = client.get("/auth/callback?state=dummy_state&code=dummy_code", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "/"

    # 이후 루트 엔드포인트 호출 시 환영 메시지가 나타나야 함
    response2 = client.get("/")
    json_data = response2.json()
    assert "Welcome" in json_data["message"]
    assert "Test User" in json_data["message"]


def test_logout_endpoint(client, monkeypatch):
    """
    로그아웃(/auth/logout) 엔드포인트가 세션에서 사용자 정보를 제거하고
    홈("/")으로 리다이렉션하는지 확인합니다.
    """
    # 먼저, /auth/callback 호출을 통해 로그인한 상태를 만듭니다.
    simulate_auth_callback(monkeypatch)
    client.get("/auth/callback?state=dummy_state&code=dummy_code", follow_redirects=False)

    # 로그인 상태에서 루트 호출 시 환영 메시지가 보여야 함
    response_before = client.get("/")
    assert "Welcome" in response_before.json()["message"]

    # 로그아웃 호출
    response_logout = client.get("/auth/logout", follow_redirects=False)
    assert response_logout.status_code == 302
    assert response_logout.headers["location"] == "/"

    # 로그아웃 후 루트 호출 시 로그인 안내 메시지가 반환되어야 함
    response_after = client.get("/")
    assert response_after.json() == {"message": "Hello, please login."}
