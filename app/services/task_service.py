from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.schemas.pagination import paginate_query

def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100, completed: bool = None):
    query = db.query(Task)
    if completed is not None:
        query = query.filter(Task.completed == completed)
    return query.offset(skip).limit(limit).all()

def get_tasks_paginated(db: Session, page: int = 1, page_size: int = 10, completed: bool = None):
    """Get tasks with proper pagination"""
    query = db.query(Task)
    if completed is not None:
        query = query.filter(Task.completed == completed)
    query = query.order_by(Task.created_at.desc())
    return paginate_query(query, page, page_size)

def update_task(db: Session, task_id: int, task_update: TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False

def get_completed_count(db: Session):
    """Custom SQL query to count completed tasks"""
    return db.query(func.count(Task.id)).filter(Task.completed == True).scalar()

def create_task_with_transaction(db: Session, task: TaskCreate):
    """Demonstrates transaction handling"""
    try:
        db_task = Task(**task.model_dump())
        db.add(db_task)
        db.flush()
        
        db_task.completed = False
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        raise e

