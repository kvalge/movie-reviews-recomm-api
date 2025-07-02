from sqlalchemy import Column, String, Text
from app.models.base_entity import BaseEntity


class Position(BaseEntity):
    __tablename__ = "positions"

    name = Column(String(256), unique=True, nullable=False)
    description = Column(Text, nullable=True)
