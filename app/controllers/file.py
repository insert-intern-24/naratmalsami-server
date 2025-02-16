import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.file import FileCreate, FileResponse
from app.services.file import create_file_service, get_files_service

logger = logging.getLogger(__name__)

async def create_file_controller(request, file_data: FileCreate, db: Session) -> FileResponse:
    """
    컨트롤러: 파일 생성 요청 처리
      - 서비스 레이어를 호출하여 파일 생성
      - 생성된 파일 객체를 반환
    """
    try:
        created_file = create_file_service(db, file_data)
        return created_file
    except Exception as e:
        logger.error("파일 생성 중 오류: %s", e)
        raise HTTPException(status_code=500, detail="파일 생성 중 내부 오류 발생.")

async def get_files_controller(request, db: Session, skip: int = 0, limit: int = 100):
    """
    컨트롤러: 파일 목록 조회 요청 처리
      - 서비스 레이어를 호출하여 파일 목록 조회
    """
    try:
        files = get_files_service(db, skip=skip, limit=limit)
        return files
    except Exception as e:
        logger.error("파일 조회 중 오류: %s", e)
        raise HTTPException(status_code=500, detail="파일 조회 중 내부 오류 발생.")
