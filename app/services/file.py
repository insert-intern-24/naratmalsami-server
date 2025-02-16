from sqlalchemy.orm import Session
from app.schemas.file import FileCreate, FileResponse
from app.crud import file as crud_file

def create_file_service(db: Session, file_data: FileCreate) -> FileResponse:
    """
    파일 생성 비즈니스 로직:
      - 전달받은 file_data를 바탕으로 DB에 파일 생성
      - 생성된 파일 객체를 반환
    """
    created_file = crud_file.create_file(db, file_data.model_dump(exclude_unset=True))
    return created_file

def get_files_service(db: Session, skip: int = 0, limit: int = 100):
    """
    파일 목록 조회 비즈니스 로직:
      - DB에서 파일 목록을 조회하여 반환
    """
    files = crud_file.get_files(db, skip=skip, limit=limit)
    return files
