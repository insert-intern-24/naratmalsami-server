from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.schemas.file import FileSave, FileHash, FileSaveResponse, FileListResponse
from app.controllers.file import create_file_controller, get_files_controller, save_file_controller, get_file_controller
from app.database import get_db

router = APIRouter(
    tags=["Files"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=FileHash, summary="파일 생성")
async def create_file_route(request: Request, db: Session = Depends(get_db)):
    """
    파일 생성 요청 처리:
      - 클라이언트가 로그인을 한 후 POST 요청을 보낼시,
      - 내부 ID를 해시화하여 반환합니다.
    """
    return await create_file_controller(request, db)
  
@router.get("/list", response_model=list[FileListResponse], summary="파일 목록 조회")
async def read_files_route(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    저장된 파일 목록을 조회합니다.
    """
    return await get_files_controller(request, db, skip=skip, limit=limit)
  
@router.get("/{hashed_id}", response_model=FileSaveResponse, summary="특정 파일 내용 조회")
async def read_file_route(request: Request, hashed_id: str, db: Session = Depends(get_db)):
  """
  파일 읽기 요청 처리:
    - 클라이언트가 특정 파일의 hashed_id 를 url 에 경로 파라미터로 보낼시,
    - 그에 해당하는 hashed_id 를 가진 파일의 내용이 반환됩니다.
  """
  return await get_file_controller(request, db, hashed_id)

@router.patch("/save", response_model=FileSaveResponse, summary="파일 저장")
async def save_file_route(request: Request, file: FileSave, db: Session = Depends(get_db)):
    """
    파일 저장 요청 처리:
      - 클라이언트가 보낸 hashed_id, title, content 등의 데이터를 받아 DB에 업데이트합니다.
    """
    return await save_file_controller(request, file, db)