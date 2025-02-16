import logging
from fastapi import Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import user as crud
from app.services.oauth import oauth

# 모듈 단위 로거 설정
logger = logging.getLogger(__name__)

async def login_controller(request: Request) -> RedirectResponse:
    """
    OAuth 로그인 플로우 시작: 인증 제공자(Google)로 리다이렉트합니다.
    """
    redirect_uri = request.url_for("auth_callback")
    try:
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as exc:
        logger.error("OAuth 로그인 플로우 시작 중 에러: %s", exc)
        raise HTTPException(status_code=500, detail="OAuth 로그인 중 내부 오류 발생.")

async def auth_callback_controller(request: Request, db: Session) -> RedirectResponse:
    """
    OAuth 콜백 처리:
      - 토큰을 받아 사용자 정보를 획득
      - DB에서 사용자 정보 생성/업데이트
      - 세션에 사용자 정보 저장 후 홈으로 리다이렉트
    """
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        logger.error("OAuth 토큰 승인 에러: %s", error)
        raise HTTPException(status_code=400, detail=f"OAuth 에러: {error}")
    except Exception as exc:
        logger.error("토큰 승인 처리 중 예상치 못한 에러: %s", exc)
        raise HTTPException(status_code=500, detail="토큰 처리 중 내부 오류 발생.")

    user_info = None
    if "id_token" in token:
        try:
            user_info = await oauth.google.parse_id_token(request, token)
        except Exception as e:
            logger.warning("id_token 파싱 실패, userinfo_endpoint로 fallback 진행. 에러: %s", e)
    
    if user_info is None:
        # userinfo_endpoint URL 검증 및 기본값 설정
        userinfo_url = oauth.google.server_metadata.get("userinfo_endpoint") or "https://openidconnect.googleapis.com/v1/userinfo"
        if not (userinfo_url.startswith("http://") or userinfo_url.startswith("https://")):
            logger.error("잘못된 userinfo_endpoint URL: %s", userinfo_url)
            raise HTTPException(status_code=500, detail="유효하지 않은 userinfo_endpoint URL.")
        try:
            resp = await oauth.google.get(userinfo_url, token=token)
            user_info = resp.json()
        except Exception as exc:
            logger.error("userinfo_endpoint 호출 실패: %s", exc)
            raise HTTPException(status_code=500, detail="사용자 정보를 가져오는 데 실패하였습니다.")

    if not user_info or "sub" not in user_info:
        logger.error("사용자 정보가 누락되었거나 올바르지 않음: %s", user_info)
        raise HTTPException(status_code=400, detail="잘못된 사용자 정보.")

    try:
        # DB에 사용자 정보 저장 또는 업데이트
        user = crud.get_user_by_google_id(db, google_id=user_info.get("sub"))
        if not user:
            user = crud.create_user(db, user_info=user_info)
        else:
            user = crud.update_user(db, user, user_info=user_info)
    except Exception as exc:
        logger.error("DB 사용자 처리 에러: %s", exc)
        raise HTTPException(status_code=500, detail="사용자 정보를 처리하는 도중 내부 오류 발생.")

    # 세션에 사용자 정보 저장
    request.session["user"] = {"id": user.id, "email": user.email, "name": user.name}
    return RedirectResponse(url="/", status_code=302)

async def logout_controller(request: Request) -> RedirectResponse:
    """
    로그아웃 처리: 세션에서 사용자 정보를 제거합니다.
    """
    request.session.pop("user", None)
    return RedirectResponse(url="/", status_code=302)
