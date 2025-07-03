import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from httpx import Client
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from main import app
from src.db.database import get_db
from src.db.models import Base

TEST_DB_URL = "sqlite:///./test_test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator[Session]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()
    if os.path.exists("test_test.db"):
        os.remove("test_test.db")


@pytest.fixture
def client(setup_db) -> Client:  # noqa: ARG001
    return TestClient(app)
