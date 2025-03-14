from sqlalchemy.orm import Session
from app.schemas.file import FileSave, FileHash
from app.crud import file as crud_file
from fastapi import HTTPException
from app.utils.authValidator import AuthValidator

def create_file_service(db: Session, request) -> FileHash:
    """
    파일 생성 비즈니스 로직:
      - 전달받은 file_data를 바탕으로 DB에 파일 생성
      - 생성된 파일 객체를 반환
    """
    user_id = AuthValidator.get_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    created_file = crud_file.create_file(db, request, user_id)
    return created_file
  
def get_file_service(db: Session, request, hashed_id):
    """
    특정 파일 조회 비즈니스 로직:
      - DB 에서 특정 hashed_id 를 가진 파일을 조회해서 내용을 반환
    """
    user_id = AuthValidator.get_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    files = crud_file.get_file(db, request, hashed_id, user_id)
    return files

def get_files_service(db: Session, request, skip: int = 0, limit: int = 100):
    """
    파일 목록 조회 비즈니스 로직:
      - DB에서 파일 목록을 조회하여 반환
    """
    user_id = AuthValidator.get_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    files = crud_file.get_files(db, request, skip=skip, limit=limit, user_id=user_id)
    return files

def save_file_service(db: Session, file_data: FileSave, request):
  """
  파일 저장 비즈니스 로직:
    - 전달받은 file_data 에서 hashed_id 를 추출
    - hashed_id 를 기반으로 변경된 내용 수정
  """
  user_id = AuthValidator.get_user_id(request)
  if not user_id:
      raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
  hashed_id = file_data.hashed_id
  
  files = crud_file.save_file(db, hashed_id, file_data.model_dump(exclude_unset=True), request, user_id)
  return files