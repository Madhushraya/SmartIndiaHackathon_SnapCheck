from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..db.database import get_async_db
from ..db.account import Account
from ..db.user import User
from ..db.device import Device
from ..schemas.auth import Token, LoginRequest, LoginResponse
from ..schemas.user import UserRegister, UserOut
from ..core.config import settings
from ..core.security import create_access_token, verify_password, hash_password

router = APIRouter()

@router.post("/auth/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Account).where(Account.email == form_data.username))
    account = result.scalars().first()
    if not account or not verify_password(form_data.password, account.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": account.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/login", response_model=LoginResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Account).where(Account.email == payload.email))
    account = result.scalars().first()
    if not account or not verify_password(payload.password, account.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    # Get user and register device
    user_result = await db.execute(select(User).where(User.account_id == account.id))
    user = user_result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user:
        device_result = await db.execute(select(Device).where(Device.device_uuid == payload.device_uuid))
        device = device_result.scalars().first()
        if not device:
            device = Device(user_id=user.id, device_uuid=payload.device_uuid, device_type=payload.device_type)
            db.add(device)
            await db.commit()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": account.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user": user}

@router.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserRegister, db: AsyncSession = Depends(get_async_db)):
    # Check if account already exists
    result = await db.execute(select(Account).where(Account.email == payload.email))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new account
    hashed_password = hash_password(payload.password)
    username = payload.username or payload.email
    new_account = Account(email=payload.email, username=username, hashed_password=hashed_password)
    db.add(new_account)
    await db.flush() # Flush to get the new_account.id

    # Create new user
    new_user = User(
        account_id=new_account.id,
        full_name=payload.full_name,
        roll_number=payload.roll_number,
        face_embedding=payload.face_embedding,
    )
    db.add(new_user)
    await db.flush() # Flush to get the new_user.id

    # Register device
    if payload.device_uuid:
        new_device = Device(
            user_id=new_user.id,
            device_uuid=payload.device_uuid,
            device_type=payload.device_type,
        )
        db.add(new_device)
    
    await db.commit()
    await db.refresh(new_user)

    return new_user
