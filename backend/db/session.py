from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from .database import Base
import uuid
from datetime import datetime

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location_lat = Column(Float, nullable=True)   # optional geofence center
    location_lng = Column(Float, nullable=True)
    geofence_radius = Column(Float, default=100)  # in meters
    
    attendances = relationship("Attendance", back_populates="session")
