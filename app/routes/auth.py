from fastapi import APIRouter, Request, Depends
from app.database import get_db
from app.controllers.auth import (
    login_controller,
    auth_callback_controller,
    logout_controller
)

router = APIRouter(
    tags=["Authentication"],
    responses={404: {"description": "Not found"}}
)

@router.get("/login", summary="OAuth 로그인 시작")
async def login(request: Request):
    """
    사용자 로그인 요청 처리:
      - OAuth 로그인 플로우를 시작합니다.
    """
    return await login_controller(request)

@router.get("/callback", name="auth_callback", summary="OAuth 콜백 처리")
async def auth_callback(request: Request, db=Depends(get_db)):
    """
    OAuth 인증 제공자에서 리다이렉트된 후 호출되는 콜백 엔드포인트.
      - 토큰 검증 후 사용자 정보를 DB에 저장/업데이트합니다.
    """
    return await auth_callback_controller(request, db)

@router.get("/logout", summary="로그아웃")
async def logout(request: Request):
    """
    사용자를 로그아웃 처리하고 홈으로 리다이렉트합니다.
    """
    return await logout_controller(request)
