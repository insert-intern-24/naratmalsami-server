from fastapi import APIRouter
from app.schemas.ai import TextData, AIForeignData, AIRefineData
from app.controllers.ai import find_foreign_controller, refine_sentence_controller
from typing import List

router = APIRouter(
    tags=["AIs"],
    responses={404: {"description": "Not found"}}
)

@router.post("/retouch", response_model=List[AIForeignData], tags=['AIs'])
async def post_ai_retouch(request: TextData):
    return find_foreign_controller(request)

@router.get("/refine", response_model=AIRefineData, tags=['AIs'])
async def get_ai_refine(request: TextData):
    return refine_sentence_controller(request)