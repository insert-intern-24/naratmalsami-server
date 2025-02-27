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
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie="session",
    domain="localhost",
    samesite="lax",
    secure=False
)
# CORS 미들웨어 등록
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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