from pydantic import BaseModel
from typing import Optional
from .user import UserOut

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str
    device_uuid: str
    device_type: str
