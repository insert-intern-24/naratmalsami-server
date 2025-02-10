from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from app.config import settings
from app.routers import auth as auth_router
from app.database import engine, Base

def create_tables():
    Base.metadata.create_all(engine)
    print("모든 테이블이 생성되었습니다.")

# create_tables()

app = FastAPI()

# 세션 미들웨어 (프로덕션에서는 Redis 등 외부 스토리지 고려)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# 인증 관련 라우터 포함 (/auth/login, /auth/callback, /auth/logout)
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])

@app.get("/")
async def root(request: Request):
    user = request.session.get("user")
    if user:
        return {"message": f"Welcome, {user.get('name')}"}
    return {"message": "Hello, please login."}
