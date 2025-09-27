from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# =======================
# Session Schemas
# =======================
class SessionBase(BaseModel):
    class_name: str
    start_time: datetime
    end_time: datetime
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    geofence_radius: Optional[float] = 100.0


class SessionCreate(SessionBase):
    pass


class SessionOut(SessionBase):
    id: int

    class Config:
        orm_mode = True
