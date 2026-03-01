import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import engine
from . import models
from .routers import users, projects, tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    for attempt in range(5):
        try:
            models.Base.metadata.create_all(bind=engine)
            break
        except Exception as e:
            if attempt == 4:
                logging.error("Failed to create database tables: %s", e)
            else:
                logging.warning("Attempt %d failed, retrying...", attempt + 1)
                time.sleep(2)
    yield

app = FastAPI(
    title="Todo API test",
    description="Multiuser Todo List with Projects",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get('/')
def root():
    return {"message": "Todo API is running. Go to /docs for documentation"}
