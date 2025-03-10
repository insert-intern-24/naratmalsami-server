from fastapi import APIRouter
from app.schemas.ai import TextData, AIRefineData
from app.controllers.ai import refine_foreign_controller
from typing import List

router = APIRouter(
    tags=["AIs"],
    responses={404: {"description": "Not found"}}
)

@router.post("/refine", response_model=List[AIRefineData], tags=['AIs'])
async def post_ai_refine(request: TextData):
    return await refine_foreign_controller(request)