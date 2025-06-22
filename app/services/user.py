from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.schemas.user import UserCreate
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        username=user.username,
        email=str(user.email),
        password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
