from fastapi import APIRouter
from app.schemas.file import File
from app.controllers.file import create_file_controller, file_list_controller
from typing import List

router = APIRouter(prefix="/file")

@router.post("/create", response_model=File, tags=['file'])
async def post_file_create():
    return create_file_controller()

@router.get("/list", response_model=List[File], tags=['file'])
async def get_file_list():
    return file_list_controller()