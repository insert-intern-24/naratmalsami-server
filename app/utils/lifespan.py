import logging
from contextlib import asynccontextmanager
from app.database import engine, Base

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app):
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("데이터베이스 테이블 생성 완료 (존재하지 않는 경우에만 생성됨).")
    except Exception as e:
        logger.exception("테이블 생성 중 오류 발생: %s", e)
        raise
    yield
    logger.info("애플리케이션 종료.")
