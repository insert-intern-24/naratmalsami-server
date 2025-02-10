from pydantic import BaseModel
from typing import Optional

class File(BaseModel):
    id: str
    title: Optional[str] = None
    content: Optional[str] = None
    datetime: str