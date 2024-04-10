import pytest
from fastapi.testclient import TestClient
from api.db_config import get_db
from api.main import app
from api.models.base import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from api.utils.auth import auth

from .fixtures import *

SQLALCHEMY_DATABASE_URL = "sqlite://"


@pytest.fixture(scope="function")
def db():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    BaseModel.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db] = lambda: TestingSessionLocal()

    session = TestingSessionLocal()

    yield session

    session.close()
    engine.dispose()


@pytest.fixture(scope="module")
def _auth():
    def override_authenticate_user():
        return {}

    app.dependency_overrides[auth] = override_authenticate_user


@pytest.fixture
def client(db, _auth):
    return TestClient(app)
