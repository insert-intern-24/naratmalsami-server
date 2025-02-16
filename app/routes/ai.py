from fastapi import APIRouter
from app.schemas.ai import TextData, AIForeignData
from app.controllers.ai import find_foreign_controller
from typing import List

router = APIRouter(
    tags=["AIs"],
    responses={404: {"description": "Not found"}}
)

@router.post("/retouch", response_model=List[AIForeignData], tags=['AIs'])
async def post_ai_retouch(request: TextData):
    return find_foreign_controller(request)