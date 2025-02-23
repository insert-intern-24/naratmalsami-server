from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    google_id: str

class UserResponse(UserBase):
    id: str
    google_id: str

    class Config:
        orm_mode = True

    model_config = ConfigDict(orm_mode=True)