from fastapi import APIRouter
from models.ai_model import TextData, AIForeignData
from controllers.ai_controller import foreign_test
from typing import List

router = APIRouter(prefix="/ai")

@router.post("/retouch", response_model=List[AIForeignData], tags=['ai'])
async def post_ai_retouch(request: TextData):
    return foreign_test(request)