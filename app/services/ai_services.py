from models.ai_model import TextData, AIForeignData
from typing import List

def find_foreign(data: TextData) -> List[AIForeignData]:
    # 여기에 외래어 구별 ai 랑 다듬은 말 가져오는 함수 적고 하면 됨
    
    return [
        AIForeignData(
            foreign="일빠",
            korean="첫번째",
            setence=["일빠 첫번째로 도착했어", "일빠 첫번째로 밥 먹을래"],
            location=[[4, 6], [20, 22]]
        ),
        AIForeignData(
            foreign="일빠",
            korean="첫번째",
            setence=["일빠 첫번째로 도착했어", "일빠 첫번째로 밥 먹을래"],
            location=[[4, 6], [20, 22]]
        )
    ]