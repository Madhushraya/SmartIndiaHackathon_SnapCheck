from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..db.item import User as UserSchema, UserCreate as UserCreateSchema
from ..db.user import User as UserModel
from ..db.database import get_async_db

router = APIRouter()

@router.post("/users/", response_model=UserSchema)
async def create_user(user: UserCreateSchema, db: AsyncSession = Depends(get_async_db)):
    db_user = UserModel(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=List[UserSchema])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(UserModel).offset(skip).limit(limit))
    users = result.scalars().all()
    return users

@router.get("/users/{user_id}", response_model=UserSchema)
async def read_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
