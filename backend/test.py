import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def test_working_sqlalchemy():
    """Test SQLAlchemy with correct syntax"""
    print("🔍 Testing SQLAlchemy with correct syntax...")
    
    DATABASE_URL = "postgresql+asyncpg://postgres.ldwddcyjguomlfspdmvh:ashwinthegreat@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"
    
    try:
        # Create engine (we know this works from previous test)
        engine = create_async_engine(
            DATABASE_URL,
            echo=True,
            pool_pre_ping=True,
            connect_args={
                "ssl": "require",
                "command_timeout": 30,
                "server_settings": {
                    "jit": "off"
                }
            }
        )
        
        print("✅ Engine created successfully")
        
        # Test with correct SQLAlchemy syntax
        async with engine.begin() as conn:
            # Use text() for raw SQL in SQLAlchemy 2.0+
            result = await conn.execute(text("SELECT 'SQLAlchemy async works!' as message"))
            message = result.fetchone()
            print(f"✅ Query result: {message[0]}")
            
            # Test another query
            version_result = await conn.execute(text("SELECT version()"))
            version = version_result.fetchone()
            print(f"✅ Database version: {version[0][:50]}...")
        
        await engine.dispose()
        print("✅ SQLAlchemy async connection fully working!")
        return True
        
    except Exception as e:
        print(f"❌ SQLAlchemy connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_table_creation():
    """Test table creation (what your init_db does)"""
    print("\n🔍 Testing table creation simulation...")
    
    DATABASE_URL = "postgresql+asyncpg://postgres.ldwddcyjguomlfspdmvh:ashwinthegreat@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"
    
    try:
        engine = create_async_engine(
            DATABASE_URL,
            echo=False,  # Reduce noise
            pool_pre_ping=True,
            connect_args={
                "ssl": "require",
                "command_timeout": 30
            }
        )
        
        async with engine.begin() as conn:
            # Simulate what your init_db() function does
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            print("✅ Table creation successful")
            
            # Test insert
            await conn.execute(text("""
                INSERT INTO test_table (name) VALUES ('FastAPI Test')
            """))
            
            print("✅ Insert successful")
            
            # Test select
            result = await conn.execute(text("SELECT * FROM test_table WHERE name = 'FastAPI Test'"))
            row = result.fetchone()
            print(f"✅ Select successful: {row}")
            
            # Cleanup
            await conn.execute(text("DROP TABLE test_table"))
            print("✅ Cleanup successful")
        
        await engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ Table operations failed: {e}")
        return False

async def main():
    print("🚀 Testing final SQLAlchemy configuration...")
    print("=" * 60)
    
    # Test basic SQLAlchemy
    basic_works = await test_working_sqlalchemy()
    
    if basic_works:
        # Test table operations
        table_works = await test_table_creation()
        
        if table_works:
            print(f"\n🎉 PERFECT! Everything works!")
            print("=" * 60)
            
            print("📝 Your working config.py:")
            print("""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Modular Boilerplate"
    PROJECT_VERSION: str = "0.1.0"
    
    DATABASE_URL: str = "postgresql+asyncpg://postgres.ldwddcyjguomlfspdmvh:ashwinthegreat@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"
    
    SECRET_KEY: str = "a_very_secret_key_that_should_be_in_a_env_file"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True

settings = Settings()
            """)
            
            print("📝 Your working database.py:")
            print("""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from ..core.config import settings

async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "ssl": "require",
        "command_timeout": 30,
        "server_settings": {"jit": "off"}
    }
)

AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
            """)
            
            print("\n🚀 NOW UPDATE YOUR FILES AND RUN:")
            print("uvicorn backend.main:app --reload")
            
        else:
            print("⚠️ Basic connection works but table operations failed")
    else:
        print("❌ Basic SQLAlchemy test failed")

if __name__ == "__main__":
    asyncio.run(main())