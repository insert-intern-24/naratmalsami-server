import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.file import FileSave, FileHash
from app.services.file import create_file_service, get_files_service, save_file_service, get_file_service

logger = logging.getLogger(__name__)

async def create_file_controller(request, db: Session) -> FileHash:
    """
    컨트롤러: 파일 생성 요청 처리
      - 서비스 레이어를 호출하여 파일 생성
      - 생성된 파일 객체를 반환
    """
    try:
        created_file = create_file_service(db, request)
        return {"hashed_id" : created_file}
    except Exception as e:
        logger.error("파일 생성 중 오류: %s", e)
        raise HTTPException(status_code=500, detail="파일 생성 중 내부 오류 발생.")

async def get_file_controller(request, db: Session, hashed_id):
  """
  컨트롤러: 특정 파일 읽기 요청 처리
  """
  try:
      files = get_file_service(db, request, hashed_id)
      return files
  except Exception as e:
      logger.error("특정 파일 조회 중 오류: %s", e)
      raise HTTPException(status_code=500, detail="특정 파일 조회 중 내부 오류 발생.")

async def get_files_controller(request, db: Session, skip: int = 0, limit: int = 100):
    """
    컨트롤러: 파일 목록 조회 요청 처리
      - 서비스 레이어를 호출하여 파일 목록 조회
    """
    try:
        files = get_files_service(db, request, skip=skip, limit=limit)
        return files
    except Exception as e:
        logger.error("파일 조회 중 오류: %s", e)
        raise HTTPException(status_code=500, detail="파일 조회 중 내부 오류 발생.")

async def save_file_controller(request, file_data: FileSave, db: Session):
  """
  컨트롤러: 파일 저장 요청 처리
    - 변경 사항들을 받아 업데이트
  """
  try:
      files = save_file_service(db, file_data, request)
      return files
  except Exception as e:
      logger.error("파일 저장 중 오류 : %s", e)
      raise HTTPException(status_code=500, detail="파일 저장 중 내부 오류 발생.")