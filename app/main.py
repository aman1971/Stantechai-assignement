from fastapi import FastAPI
from app.routes.task_routes import router as task_router
from app.routes.api_key_routes import router as api_key_router

app = FastAPI(
    title="Task Management API",
    description="A simple CRUD API for managing tasks with API Key authentication and pagination",
    version="2.0.0"
)

app.include_router(api_key_router)
app.include_router(task_router)

@app.get("/")
def root():
    return {"message": "Task Management API is running"}

