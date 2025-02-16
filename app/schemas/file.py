from pydantic import BaseModel, ConfigDict
from datetime import datetime

class FileBase(BaseModel):
    title: str
    content: str

class FileCreate(FileBase):
    # 클라이언트에서 날짜를 보내는 경우
    created_at: datetime | None = None  
    updated_at: datetime | None = None

class FileResponse(FileBase):
    id: int
    hashed_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
