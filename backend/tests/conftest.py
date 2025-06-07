import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
import pytest
from fastapi.testclient import TestClient
from app.core.security import get_password_hash, create_access_token
from app.database import get_db, User, Base, engine
from app.main import app

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """ Set up the SQLite database for testing """
    if "sqlite" not in str(engine.url):
        raise RuntimeError("Test DB is not SQLite!")
    Base.metadata.create_all(bind=engine) 
    yield
    Base.metadata.drop_all(bind=engine)

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

@pytest.fixture(autouse=True)
def clean_tables():
    yield
    # After each test, remove all rows from all tables
    with engine.connect() as conn:
        trans = conn.begin()
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        trans.commit()

@pytest.fixture(scope="session", autouse=True)
def remove_test_db(request):
    # This runs after all tests are finished
    def cleanup():
        try:
            os.remove("test.db")
        except FileNotFoundError:
            pass
    request.addfinalizer(cleanup)
