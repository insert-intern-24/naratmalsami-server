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