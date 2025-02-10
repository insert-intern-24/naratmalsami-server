from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError
from sqlalchemy.orm import Session
from app.config import settings
from app.database import SessionLocal
from app.crud import user as crud
from app.services.oauth import oauth

router = APIRouter()

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback", name="auth_callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        raise HTTPException(status_code=400, detail=f"OAuth Error: {error}")

    user_info = None
    if "id_token" in token:
        try:
            user_info = await oauth.google.parse_id_token(request, token)
        except Exception as e:
            print("id_token 파싱 오류, fallback 진행:", e)
    if user_info is None:
        userinfo_url = oauth.google.server_metadata.get("userinfo_endpoint")
        if not userinfo_url:
            userinfo_url = "https://openidconnect.googleapis.com/v1/userinfo"
        if not (userinfo_url.startswith("http://") or userinfo_url.startswith("https://")):
            raise HTTPException(status_code=500, detail="userinfo_endpoint URL이 올바르지 않습니다.")
        resp = await oauth.google.get(userinfo_url, token=token)
        user_info = resp.json()

    # DB에 사용자 정보 저장 또는 업데이트
    user = crud.get_user_by_google_id(db, google_id=user_info.get("sub"))
    if not user:
        user = crud.create_user(db, user_info=user_info)
    else:
        user = crud.update_user(db, user, user_info=user_info)

    # 세션에 사용자 정보 저장
    request.session["user"] = {"id": user.id, "email": user.email, "name": user.name}
    return RedirectResponse(url="/")

@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")


# 172.26.160.1
# insertnara