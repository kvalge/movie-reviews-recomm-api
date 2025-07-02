from sqlalchemy import Column, String, Text
from app.models.base_entity import BaseEntity


class Genre(BaseEntity):
    __tablename__ = "genres"

    name = Column(String(256), unique=True, nullable=False)
    description = Column(Text, nullable=True)