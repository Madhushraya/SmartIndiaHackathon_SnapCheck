from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from .database import Base
import uuid
from datetime import datetime

class Attendance(Base):
    __tablename__ = "attendances"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    face_embedding = Column(String, nullable=False)  
    liveness_passed = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="attendances")
    session = relationship("Session", back_populates="attendances")
    device = relationship("Device")
