from app.services.ai import refine_foreign
from app.schemas.ai import TextData

def refine_foreign_controller(data: TextData):
    """
    요청받은 문장 중 외래어를 찾고 다듬어서 변환합니다.
    """
    return refine_foreign(data)