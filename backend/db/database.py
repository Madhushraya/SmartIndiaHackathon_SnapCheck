from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from sqlalchemy.exc import SQLAlchemyError
import asyncio
import logging
from uuid import uuid4
from ..core.config import settings

logger = logging.getLogger(__name__)

# Create async engine with the working configuration
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    poolclass=NullPool,
    connect_args={
        "ssl": settings.DB_SSL_REQUIRE,
        "command_timeout": settings.DB_COMMAND_TIMEOUT,
        "server_settings": {
            "jit": "off" if settings.DB_JIT_OFF else "on"
        },
        "statement_cache_size": settings.DB_STATEMENT_CACHE_SIZE,
        "prepared_statement_name_func": lambda: f"__asyncpg_{uuid4()}__",
    }
)

AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def init_db():
    """Initialize database with retry logic"""
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting database initialization (attempt {attempt + 1}/{max_retries})")
            
            async with asyncio.timeout(30):
                async with async_engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
                    logger.info("✅ Database initialization successful")
                    return
                    
        except asyncio.TimeoutError:
            logger.error(f"⏱️ Database connection timeout on attempt {attempt + 1}")
            if attempt < max_retries - 1:
                logger.info(f"🔄 Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error("❌ All database connection attempts failed due to timeout")
                raise
                
        except SQLAlchemyError as e:
            logger.error(f"❌ Database error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                logger.info(f"🔄 Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error("❌ All database connection attempts failed")
                raise
                
        except Exception as e:
            logger.error(f"❌ Unexpected error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                logger.info(f"🔄 Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error("❌ All database connection attempts failed")
                raise

async def get_async_db():
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()

# Optional: Test connection function
async def test_connection():
    """Test database connection"""
    try:
        async with async_engine.begin() as conn:
            result = await conn.execute("SELECT 1")
            logger.info("✅ Database connection test successful")
            return True
    except Exception as e:
        logger.error(f"❌ Database connection test failed: {e}")
        return False