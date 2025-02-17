from pydantic import BaseModel, ConfigDict
from datetime import datetime

class FileBase(BaseModel):
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: str
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M") if v else None
        }
    
class FileHash(BaseModel):
    hashed_id: str
    
class FileSave(BaseModel):
    title: str
    content: str
    hashed_id: str

class FileSaveResponse(FileSave):
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M") if v else None
        }

class FileResponse(FileBase):
    id: int
    hashed_id: str

    model_config = ConfigDict(from_attributes=True)
