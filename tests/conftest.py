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
import pytest

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