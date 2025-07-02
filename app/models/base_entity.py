from sqlalchemy import Column, Integer
from app.db.session import Base


class BaseEntity(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)