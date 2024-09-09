import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.models import Base
from app.db.connection import get_db
from app.use_cases.role import RoleUseCases


@pytest.fixture
def client(session):
    def get_db_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_db] = get_db_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:',
                        connect_args={'check_same_thread': False},
        poolclass=StaticPool,   
                        )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    # Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)

@pytest.fixture
def role_use_cases(session):
    return RoleUseCases(session)