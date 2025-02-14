from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from app.config import settings
from app.utils.logging import setup_logging
from app.utils.lifespan import lifespan
from app.routes import ai, auth as auth_router, file

# 로깅 설정
setup_logging()

app = FastAPI(lifespan=lifespan)

# 세션 미들웨어 등록
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# API 라우터 등록
app.include_router(auth_router.router, tags=["auth"])
app.include_router(ai.router)
app.include_router(file.router)

@app.get("/")
async def root(request: Request):
    user = request.session.get("user")
    if user:
        return {"message": f"Welcome, {user.get('name')}"}
    return {"message": "Hello, please login."}
