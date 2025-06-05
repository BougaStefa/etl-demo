import pytest
from fastapi.testclient import TestClient
from app.core.security import get_password_hash, create_access_token
from app.database import get_db, User
from app.main import app

@pytest.fixture
def client():
    """ FastAPI test client for testing"""
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    """ Valid JWT auth headers for testing, ensures user exists """
    db = next(get_db())
    username = "testuser"
    password = "testpass"
    # Create user if not exists
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(
            username=username,
            email=None,
            hashed_password=get_password_hash(password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    token = create_access_token(data={"sub": username})
    return {"Authorization": f"Bearer {token}"}
