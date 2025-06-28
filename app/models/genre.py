from sqlalchemy import Column, BigInteger, String, Text
from app.db.session import Base

class Genre(Base):
    __tablename__ = "genres"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(256), unique=True, nullable=False)
    description = Column(Text, nullable=True)
