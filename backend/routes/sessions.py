from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.database import get_async_db
from ..schemas.session import SessionOut
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/sessions/current", response_model=SessionOut)
async def get_current_session(db: AsyncSession = Depends(get_async_db)):
    """ 
    Returns the current active session.
    For now, it returns a hardcoded session.
    """
    now = datetime.utcnow()
    return SessionOut(
        id=1,
        class_name="Test Class",
        start_time=now - timedelta(hours=1),
        end_time=now + timedelta(hours=1),
        location_lat=12.34,
        location_lng=56.78,
        geofence_radius=100.0
    )
