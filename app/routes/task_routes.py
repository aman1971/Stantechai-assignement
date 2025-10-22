from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.pagination import PaginationParams, PaginatedResponse
from app.services import task_service
from app.utils.security import verify_api_key

router = APIRouter(prefix="/items", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    api_key = Depends(verify_api_key)
):
    try:
        return task_service.create_task(db, task)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Task with this title already exists")

@router.get("/", response_model=PaginatedResponse[TaskResponse])
def read_tasks(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    completed: Optional[bool] = Query(None, description="Filter by completed status"),
    db: Session = Depends(get_db),
    api_key = Depends(verify_api_key)
):
    """
    Get paginated list of tasks
    
    - **page**: Page number (starts from 1)
    - **page_size**: Number of items per page (1-100)
    - **completed**: Optional filter by completion status
    
    Returns paginated response with items and pagination metadata
    """
    items, pagination_meta = task_service.get_tasks_paginated(
        db, page=page, page_size=page_size, completed=completed
    )
    return PaginatedResponse(items=items, pagination=pagination_meta)

@router.get("/{id}", response_model=TaskResponse)
def read_task(
    id: int,
    db: Session = Depends(get_db),
    api_key = Depends(verify_api_key)
):
    db_task = task_service.get_task(db, id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/{id}", response_model=TaskResponse)
def update_task(
    id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    api_key = Depends(verify_api_key)
):
    db_task = task_service.update_task(db, id, task)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{id}", status_code=204)
def delete_task(
    id: int,
    db: Session = Depends(get_db),
    api_key = Depends(verify_api_key)
):
    if not task_service.delete_task(db, id):
        raise HTTPException(status_code=404, detail="Task not found")
    return None

