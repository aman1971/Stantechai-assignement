import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Management API is running"}

def test_create_task(client):
    response = client.post("/items/", json={
        "title": "New Task",
        "description": "Task description",
        "completed": False
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Task"
    assert data["description"] == "Task description"
    assert "id" in data

def test_create_duplicate_task(client):
    client.post("/items/", json={"title": "Duplicate Task"})
    response = client.post("/items/", json={"title": "Duplicate Task"})
    assert response.status_code == 400

def test_read_tasks(client):
    client.post("/items/", json={"title": "Task 1"})
    client.post("/items/", json={"title": "Task 2"})
    
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

def test_read_tasks_with_pagination(client):
    for i in range(5):
        client.post("/items/", json={"title": f"Task {i}"})
    
    response = client.get("/items/?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_read_tasks_with_filter(client):
    client.post("/items/", json={"title": "Completed Task", "completed": True})
    client.post("/items/", json={"title": "Incomplete Task", "completed": False})
    
    response = client.get("/items/?completed=true")
    assert response.status_code == 200
    data = response.json()
    assert all(task["completed"] for task in data)

def test_read_single_task(client):
    create_response = client.post("/items/", json={"title": "Single Task"})
    task_id = create_response.json()["id"]
    
    response = client.get(f"/items/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Single Task"

def test_read_nonexistent_task(client):
    response = client.get("/items/9999")
    assert response.status_code == 404

def test_update_task(client):
    create_response = client.post("/items/", json={"title": "Original Title"})
    task_id = create_response.json()["id"]
    
    response = client.put(f"/items/{task_id}", json={
        "title": "Updated Title",
        "completed": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["completed"] == True

def test_update_nonexistent_task(client):
    response = client.put("/items/9999", json={"title": "Updated"})
    assert response.status_code == 404

def test_delete_task(client):
    create_response = client.post("/items/", json={"title": "To Delete"})
    task_id = create_response.json()["id"]
    
    response = client.delete(f"/items/{task_id}")
    assert response.status_code == 204
    
    get_response = client.get(f"/items/{task_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_task(client):
    response = client.delete("/items/9999")
    assert response.status_code == 404

