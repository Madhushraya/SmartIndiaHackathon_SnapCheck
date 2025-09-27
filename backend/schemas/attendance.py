from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# =======================
# Attendance Schemas
# =======================
class AttendanceBase(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    face_embedding: str
    liveness_passed: bool = False


class AttendanceCreate(AttendanceBase):
    user_id: int
    session_id: int
    device_id: int


class AttendanceOut(AttendanceBase):
    id: int
    user_id: int
    session_id: int
    device_id: int
    timestamp: datetime

    class Config:
        orm_mode = True
