from typing import Optional

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.schemas.user import UserCreate
from app.models.user import User
import re

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


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, identifier: str, password: str) -> Optional[User]:
    is_email = bool(re.match(r"[^@]+@[^@]+\.[^@]+", identifier))

    if is_email:
        user = db.query(User).filter(User.email == identifier).first()
    else:
        user = db.query(User).filter(User.username == identifier).first()

    if not user or not verify_password(password, user.password):
        return None

    return user
