import os

import pymongo
import pytest
from fastapi.testclient import TestClient
from pymongo.database import Database

from config import config
from data_fixtures import USER, PASSWORD, ADMIN_USER
from main import app


@pytest.fixture(scope="module")
def test_app() -> TestClient:
    """Create a test client for the FastAPI app."""
    client = TestClient(app)
    yield client


@pytest.fixture(scope="function")
def db() -> Database:
    """Create a clean database for each test."""
    client = pymongo.MongoClient(config.db_url)
    db = client.get_database(config.db_name)
    yield db
    client.drop_database(config.db_name)
    client.close()


@pytest.fixture(scope="function")
def user_access_token(db, test_app) -> str:
    """Create a user and return an access token for that user."""
    db.users.insert_one(USER)

    # Get access token
    response = test_app.post(
        "/auth/token",
        data={"username": USER["username"], "password": PASSWORD},
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def admin_access_token(db, test_app) -> str:
    """Create a user with admin role and return an access token for that user."""
    db.users.insert_one(ADMIN_USER)

    # Get access token
    response = test_app.post(
        "/auth/token",
        data={"username": ADMIN_USER["username"], "password": PASSWORD},
    )
    return response.json()["access_token"]
