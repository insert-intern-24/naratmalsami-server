from pydantic import BaseModel
from typing import List

class TextData(BaseModel):
    title: str
    content: List[str]

class AIError(BaseModel):
    code: int
    origin_word: str
    refine_word: List[str]
    index: int

class AIRefineData(BaseModel):
    target_id: str
    error: List[AIError]
    
class DifyInput(BaseModel):
    origin_word: List[str]
    sentence: str