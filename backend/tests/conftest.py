import pytest
from fastapi.testclient import TestClient
from app.core.security import create_access_token
from app.main import app

@pytest.fixture
def client():
    """ FastAPI test client for testing"""
    return TestClient(app)

@pytest.fixture
def auth_headers():
    """ Valid JWT auth headers for testing"""
    token = create_access_token(data={"sub": "testuser"})
    return {"Authorization": f"Bearer {token}"}
