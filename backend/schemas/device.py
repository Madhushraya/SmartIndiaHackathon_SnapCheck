from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# =======================
# Device Schemas
# =======================
class DeviceBase(BaseModel):
    device_uuid: str
    device_type: Optional[str] = None


class DeviceCreate(DeviceBase):
    user_id: int


class DeviceOut(DeviceBase):
    id: int
    user_id: int
    last_seen: datetime

    class Config:
        orm_mode = True
