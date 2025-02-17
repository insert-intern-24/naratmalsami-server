from pydantic import BaseModel, ConfigDict
from datetime import datetime

class FileBase(BaseModel):
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: str
    
class FileHash(BaseModel):
    hashed_id: str
    
class FileSave(FileBase):
    hashed_id: str
    updated_at: datetime

class FileResponse(FileBase):
    id: int
    hashed_id: str

    model_config = ConfigDict(from_attributes=True)
