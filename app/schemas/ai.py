from pydantic import BaseModel
from typing import List

class TextData(BaseModel):
    title: str
    content: str

class AIForeignData(BaseModel):
    foreign: str
    korean: str
    setence: List[str]
    location: List[List[int]]

class AIError(BaseModel):
    code: int
    origin_word: str
    refine_word: str
    index: int

class AIRefineData(BaseModel):
    target_id: str
    error: List[AIError]