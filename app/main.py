from fastapi import FastAPI
from .database import engine
from . import models
from .routers import users, projects, tasks

app = FastAPI(
    title = "Todo API test",
    description="Multiuser Todo List with Projects",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():

    import logging, time
    for attempt in range(5):
        try:
            models.Base.metadata.create_all(bind=engine)
            break
        except Exception as e:
            
            if attempt == 4:
                logging.error(
                    "Failed to create database tables after retries: %s", e
                )
            else:
                logging.warning("Could not create database tables (attempt %d): %s", attempt + 1, e)
                time.sleep(2)

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get('/')
def root():
    return {"message": "Todo API is running. Go to /docs for documentation"}