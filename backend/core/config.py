from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Modular Boilerplate"
    PROJECT_VERSION: str = "0.1.0"
    DATABASE_URL: str = "postgresql+asyncpg://postgres.ldwddcyjguomlfspdmvh:ashwinthegreat@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"

    # Database settings
    DB_ECHO: bool = True
    DB_POOL_PRE_PING: bool = True
    DB_POOL_RECYCLE: int = 300
    DB_SSL_REQUIRE: str = "require"
    DB_COMMAND_TIMEOUT: int = 30
    DB_JIT_OFF: bool = True
    DB_STATEMENT_CACHE_SIZE: int = 0
    DB_PREPARED_STATEMENT_CACHE_SIZE: int = 0
    

    # Security
    SECRET_KEY: str = "a_very_secret_key_that_should_be_in_a_env_file"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True

settings = Settings()
