from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    full_name: str
    roll_number: str
    face_embedding: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    account_id: int
    created_at: datetime

    class Config:
        orm_mode = True