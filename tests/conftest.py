import pytest
import warnings
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.core import Base
from src.entities.user import User
from src.entities.todo import Todo
from src.auth.model import TokenData   
from src.auth.service import get_password_hash
from src.rate_limiting import limiter   


@pytest.fixture(scope="function")
def db_session():
    # Use a unique database URL for testing
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        
@pytest.fixture(scope="function")
def test_user():
    # Create a user with a known password hash
    password_hash = get_password_hash("password123")
    return User(
        id=uuid4(),
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password_hash=password_hash
    )
    

@pytest.fixture(scope="function")
def test_token_data():
    return TokenData(user_id=str(uuid4()))

@pytest.fixture(scope="function")
def test_todo(test_token_data):
    return Todo(
        id=uuid4(),
        description="Test Description",
        is_completed=False,
        created_at=datetime.now(timezone.utc),
        user_id=test_token_data.get_uuid()  
    )
    
 
@pytest.fixture(scope="function")
def client(db_session):
    from src.main import app
    from src.database.core import get_db
    
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    from fastapi.testclient import TestClient
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
    

@pytest.fixture(scope="function")
def auth_headers(client, db_session):
    # Register a test user
    response = client.post(
        "/auth/register",
        json={
            "email": "test.user@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    assert response.status_code == 201, "User registration failed"

    # Login with the test user
    login_response = client.post(
        "/auth/login",
        data={
            "username": "test.user@example.com",
            "password": "testpassword123"
        }
    )
    assert login_response.status_code == 200, "User login failed"
    
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="function")
def client(db_session):
    from src.main import app
    from src.database.core import get_db
    from fastapi.testclient import TestClient

    # Disable rate limiting for tests
    if hasattr(app.state, 'limiter'):
        app.state.limiter.reset()
    # Alternative if using FastAPI-Limiter directly:
    # from fastapi_limiter import FastAPILimiter
    # FastAPILimiter.reset()

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.rollback()  # Ensure no partial commits remain
            db_session.close()

    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db

    # Create and yield test client
    with TestClient(app) as test_client:
        yield test_client

    # Clean up after test completes
    app.dependency_overrides.clear()
    

@pytest.fixture(scope="function")
def auth_headers(client, db_session):
    """Fixture to provide authentication headers for tests"""
    
    # 1. Register test user
    register_response = client.post(
        "/auth/register",
        json={
            "email": "test.user@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    
    # Fixed: Use the actual response variable
    assert register_response.status_code == 201, \
        f"Registration failed: {register_response.text}"

    # 2. Login to get access token
    login_response = client.post(
        "/auth/token",
        data={
            "username": "test.user@example.com",
            "password": "testpassword123",
            "grant_type": "password"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    # Fixed: Use the actual response variable
    assert login_response.status_code == 200, \
        f"Login failed: {login_response.text}"

    # 3. Extract and return auth headers
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}