from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from app.config import settings
from app.utils.logging import setup_logging
from app.utils.lifespan import lifespan
from app.routes import ai, auth as auth_router, files

# 로깅 설정
setup_logging()

app = FastAPI(lifespan=lifespan)

# 세션 미들웨어 등록
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# CORS 미들웨어 등록
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용, 필요에 따라 특정 도메인으로 변경
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# API 라우터 등록
app.include_router(ai.router, prefix="/ai")
app.include_router(auth_router.router, prefix="/auth")
app.include_router(files.router, prefix="/files")


@app.get("/")
async def root(request: Request):
    user = request.session.get("user")
    if user:
        print(user.get('id'))
        return {"message": f"Welcome, {user.get('name')}"}
    return {"message": "Hello, please login."}