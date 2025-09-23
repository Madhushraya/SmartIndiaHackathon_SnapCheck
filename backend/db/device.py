from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import uuid
from datetime import datetime

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_uuid = Column(String, unique=True, nullable=False)
    device_type = Column(String)  # e.g., 'android', 'ios', 'desktop'
    last_seen = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="devices")
