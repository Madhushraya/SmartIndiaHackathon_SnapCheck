from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# =======================
# Account Schemas
# =======================
class AccountBase(BaseModel):
    email: EmailStr
    username: str


class AccountCreate(AccountBase):
    password: str   # plain text input, will be hashed before DB insert


class AccountOut(AccountBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# =======================
# User Schemas
# =======================
class UserBase(BaseModel):
    full_name: str
    roll_number: str
    face_embedding: Optional[str] = None


class UserCreate(UserBase):
    account_id: int


class UserOut(UserBase):
    id: int
    account_id: int
    class Config:
        from_attributes = True

class UserRegister(BaseModel):
    # account info
    email: EmailStr
    username: Optional[str] = None
    password: str = Field(min_length=6)

    # user info
    full_name: str
    roll_number: str
    face_embedding: Optional[str] = None

    # device info
    device_uuid: Optional[str] = None
    device_type: Optional[str] = None

    class Config:
        orm_mode = True
