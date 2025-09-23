from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from .database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    full_name = Column(String, nullable=False)
    roll_number = Column(String, unique=True, nullable=False)
    face_embedding = Column(String, nullable=False)  # store as JSON or array string
    created_at = Column(DateTime, default=datetime.utcnow)
    
    account = relationship("Account", back_populates="users")
    devices = relationship("Device", back_populates="user")
    attendances = relationship("Attendance", back_populates="user")