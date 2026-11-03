from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from app.routers import router
from app.db import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    
app = FastAPI(title="Authentication Demo APIs", lifespan=lifespan)
app.include_router(router, prefix="/api")