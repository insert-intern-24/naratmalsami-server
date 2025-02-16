from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.schemas.file import FileCreate, FileResponse
from app.controllers.file import create_file_controller, get_files_controller
from app.database import SessionLocal, get_db

router = APIRouter(
    tags=["Files"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=FileResponse, summary="파일 생성")
async def create_file_route(request: Request, file: FileCreate, db: Session = Depends(get_db)):
    """
    파일 생성 요청 처리:
      - 클라이언트가 보낸 title, content, datetime 등의 데이터를 받아 DB에 저장하고,
      - 내부 ID를 해시화하여 반환합니다.
    """
    return await create_file_controller(request, file, db)

@router.get("/", response_model=list[FileResponse], summary="파일 목록 조회")
async def read_files_route(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    저장된 파일 목록을 조회합니다.
    """
    return await get_files_controller(request, db, skip=skip, limit=limit)
