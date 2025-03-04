from app.services.ai import find_foreign, refine_sentence
from app.schemas.ai import TextData

def find_foreign_controller(data: TextData):
    return find_foreign(data)

async def refine_sentence_controller(data: TextData):
    """
    요청받은 문장을 순화하여 반환합니다.
    """
    return refine_sentence(data)