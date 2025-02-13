import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.routes import ai, auth as auth_router, file
from app.database import engine, Base

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("데이터베이스 테이블 생성 완료 (존재하지 않는 경우에만 생성됨).")
    except Exception as e:
        logger.exception("테이블 생성 중 오류 발생: %s", e)
        raise
    yield
    logger.info("애플리케이션 종료.")

app = FastAPI(lifespan=lifespan, debug=settings.debug)

# 세션 미들웨어 설정
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# 라우터 등록
app.include_router(auth_router.router, tags=["auth"])
app.include_router(ai.router)
app.include_router(file.router)

@app.get("/")
async def root(request: Request):
    user = request.session.get("user")
    if user:
        return {"message": f"Welcome, {user.get('name')}"}
    return {"message": "Hello, please login."}
