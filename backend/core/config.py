from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Modular Boilerplate"
    PROJECT_VERSION: str = "0.1.0"
    DATABASE_URL: str = "postgresql+asyncpg://postgres.ldwddcyjguomlfspdmvh:ashwinthegreat@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"

    class Config:
        case_sensitive = True

settings = Settings()
