import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.services import task_service

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_task(db):
    task_data = TaskCreate(title="Test Task", description="Test Description")
    task = task_service.create_task(db, task_data)
    
    assert task.id is not None
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed == False

def test_get_task(db):
    task_data = TaskCreate(title="Get Test", description="Get Description")
    created_task = task_service.create_task(db, task_data)
    
    retrieved_task = task_service.get_task(db, created_task.id)
    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == "Get Test"

def test_get_tasks_with_filter(db):
    task_service.create_task(db, TaskCreate(title="Task 1", completed=True))
    task_service.create_task(db, TaskCreate(title="Task 2", completed=False))
    
    completed_tasks = task_service.get_tasks(db, completed=True)
    assert len(completed_tasks) == 1
    assert completed_tasks[0].title == "Task 1"

def test_update_task(db):
    task_data = TaskCreate(title="Update Test", description="Original")
    created_task = task_service.create_task(db, task_data)
    
    update_data = TaskUpdate(description="Updated", completed=True)
    updated_task = task_service.update_task(db, created_task.id, update_data)
    
    assert updated_task.description == "Updated"
    assert updated_task.completed == True
    assert updated_task.title == "Update Test"

def test_delete_task(db):
    task_data = TaskCreate(title="Delete Test")
    created_task = task_service.create_task(db, task_data)
    
    result = task_service.delete_task(db, created_task.id)
    assert result == True
    
    deleted_task = task_service.get_task(db, created_task.id)
    assert deleted_task is None

def test_get_completed_count(db):
    task_service.create_task(db, TaskCreate(title="Task 1", completed=True))
    task_service.create_task(db, TaskCreate(title="Task 2", completed=True))
    task_service.create_task(db, TaskCreate(title="Task 3", completed=False))
    
    count = task_service.get_completed_count(db)
    assert count == 2

def test_transaction_handling(db):
    task_data = TaskCreate(title="Transaction Test", description="Test")
    task = task_service.create_task_with_transaction(db, task_data)
    
    assert task.id is not None
    assert task.completed == False

