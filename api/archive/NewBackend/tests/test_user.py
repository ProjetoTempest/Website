import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from newbackend.main import app 
from newbackend.database import Base, get_db
from newbackend.schemas import UserCreate, UserUpdate
from newbackend.controllers import user_controller

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user(test_db):
    response = client.post(
        "/users/",
        json={
    "id": 0,
    "name": "string",
    "email": "testuser@example.com",
    "role_id": 0,
    "photo": "string",
    "description": "string",
    "password": "secret"
  }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"

def test_read_user(test_db):
    user = user_controller.create_user(db=next(override_get_db()), user=UserCreate(id=0, name = "string", email= "testuser@example.com", role_id=0,photo="string", description= "string", password="secret"))
    
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"

def test_update_email(test_db):
    user = user_controller.create_user(db=next(override_get_db()), user=UserCreate(id=0, name = "string", email= "testuser@example.com", role_id=0,photo="string", description= "string", password="secret"))
    
    response = client.put(f"/users/upadate_email/new@example.com/{user.email}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "new@example.com"

def test_delete_user(test_db):
    user = user_controller.create_user(db=next(override_get_db()), user=UserCreate(id=0, name = "string", email= "testuser@example.com", role_id=0,photo="string", description= "string", password="secret"))
    
    response = client.delete(f"/users/delete/{user.email}/{user.password}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User deleted successfully"
