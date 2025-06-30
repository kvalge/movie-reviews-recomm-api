from sqlalchemy.orm import Session

from app.services.user import create_user, get_user_by_id, get_user_by_email
from app.schemas.user import UserCreate

def test_create_user_success(db_session: Session, sample_user_data):
    """Test successful user creation in service layer."""
    user_create = UserCreate(**sample_user_data)
    user = create_user(db_session, user_create)
    
    assert user.email == sample_user_data["email"]
    assert user.username == sample_user_data["username"]
    assert user.id is not None

def test_get_user_by_id_success(db_session: Session, sample_user_data):
    """Test getting user by ID in service layer."""
    user_create = UserCreate(**sample_user_data)
    created_user = create_user(db_session, user_create)
    
    retrieved_user = get_user_by_id(db_session, created_user.id)
    assert retrieved_user is not None
    assert retrieved_user.email == sample_user_data["email"]

def test_get_user_by_email_success(db_session: Session, sample_user_data):
    """Test getting user by email in service layer."""
    user_create = UserCreate(**sample_user_data)
    created_user = create_user(db_session, user_create)
    
    retrieved_user = get_user_by_email(db_session, sample_user_data["email"])
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id

def test_get_user_by_id_not_found(db_session: Session):
    """Test getting non-existent user by ID returns None."""
    user = get_user_by_id(db_session, 999)
    assert user is None

def test_get_user_by_email_not_found(db_session: Session):
    """Test getting non-existent user by email returns None."""
    user = get_user_by_email(db_session, "nonexistent@example.com")
    assert user is None 