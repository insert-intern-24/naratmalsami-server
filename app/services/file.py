from sqlalchemy.orm import Session
from app.schemas.file import FileResponse, FileSave, FileHash
from app.crud import file as crud_file

def create_file_service(db: Session, request) -> FileHash:
    """
    파일 생성 비즈니스 로직:
      - 전달받은 file_data를 바탕으로 DB에 파일 생성
      - 생성된 파일 객체를 반환
    """
    created_file = crud_file.create_file(db, request)
    return created_file

def get_files_service(db: Session, skip: int = 0, limit: int = 100):
    """
    파일 목록 조회 비즈니스 로직:
      - DB에서 파일 목록을 조회하여 반환
    """
    files = crud_file.get_files(db, skip=skip, limit=limit)
    return files

def save_file_service(db: Session, file_data: FileSave):
  """
  파일 저장 비즈니스 로직:
    - 전달받은 file_data 에서 hashed_id 를 추출
    - hashed_id 를 기반으로 변경된 내용 수정
  """
  hashed_id = file_data.hashed_id
  
  files = crud_file.save_file(db, hashed_id, file_data.model_dump(exclude_unset=True))
  return files