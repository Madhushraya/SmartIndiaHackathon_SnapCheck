from fastapi import FastAPI
from .routes import auth, sessions, attendance
from backend.db.database import init_db, async_engine # Import init_db and async_engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FastAPI Modular Boilerplate",
    description="A modular FastAPI application structure.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_db() # Call init_db on startup

@app.on_event("shutdown")
async def shutdown():
    await async_engine.dispose()

app.include_router(auth.router, prefix="/api/v1")
app.include_router(sessions.router, prefix="/api/v1", tags=["sessions"])
app.include_router(attendance.router, prefix="/api/v1", tags=["attendance"])

@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to the FastAPI Modular Boilerplate!"}
