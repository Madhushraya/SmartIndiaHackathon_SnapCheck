from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ..db.database import get_async_db
from ..db.attendance import Attendance
from ..db.user import User
from ..db.device import Device
from ..schemas.attendance import AttendanceCreate, AttendanceOut
from ..core.security import get_current_user

router = APIRouter()

@router.post("/attendance/submit", response_model=AttendanceOut)
async def submit_attendance(payload: AttendanceCreate, db: AsyncSession = Depends(get_async_db), current_user: User = Depends(get_current_user)):
    # Get device id
    device_result = await db.execute(select(Device).where(Device.user_id == current_user.id))
    device = device_result.scalars().first()
    if not device:
        raise HTTPException(status_code=400, detail="Device not found for user")

    new_attendance = Attendance(
        user_id=current_user.id,
        session_id=payload.session_id,
        device_id=device.id,
        latitude=payload.latitude,
        longitude=payload.longitude,
        face_embedding=payload.face_embedding,
        liveness_passed=payload.liveness_passed
    )
    db.add(new_attendance)
    await db.commit()
    await db.refresh(new_attendance)
    return new_attendance

@router.get("/attendance/recent", response_model=List[AttendanceOut])
async def get_recent_attendance(db: AsyncSession = Depends(get_async_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Attendance)
        .where(Attendance.user_id == current_user.id)
        .order_by(Attendance.timestamp.desc())
        .limit(10)
    )
    return result.scalars().all()

@router.get("/attendance/stats")
async def get_attendance_stats(db: AsyncSession = Depends(get_async_db), current_user: User = Depends(get_current_user)):
    total_sessions_query = await db.execute(select(func.count()).select_from(select(Attendance.session_id).where(Attendance.user_id == current_user.id).distinct()))
    total_sessions = total_sessions_query.scalar_one()

    present_count_query = await db.execute(
        select(func.count())
        .where(Attendance.user_id == current_user.id, Attendance.liveness_passed == True)
    )
    present_count = present_count_query.scalar_one()

    attendance_percentage = (present_count / total_sessions * 100) if total_sessions > 0 else 0

    return {
        "totalSessions": total_sessions,
        "presentCount": present_count,
        "attendancePercentage": round(attendance_percentage, 2)
    }
