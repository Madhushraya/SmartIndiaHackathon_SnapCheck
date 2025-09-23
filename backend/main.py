from fastapi import FastAPI
from .routes import items
from backend.db.database import init_db # Import init_db

app = FastAPI(
    title="FastAPI Modular Boilerplate",
    description="A modular FastAPI application structure.",
    version="0.1.0",
)

@app.on_event("startup")
async def startup():
    await init_db() # Call init_db on startup

# No shutdown event needed for SQLAlchemy async session management as it's handled by get_async_db

app.include_router(items.router, prefix="/api/v1", tags=["items"])

@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to the FastAPI Modular Boilerplate!"}
