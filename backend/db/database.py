from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from ..core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)

AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def init_db():
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Use with caution!
        await conn.run_sync(Base.metadata.create_all)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
