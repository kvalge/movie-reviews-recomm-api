from sqlalchemy import Column, String, Text, Date
from app.models.base_entity import BaseEntity


class CastAndCrew(BaseEntity):
    __tablename__ = "cast_and_crew"

    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    stage_name = Column(String(256), nullable=False)
    birth_date = Column(Date, nullable=True)
    image_url = Column(String(2048), nullable=True)
    description = Column(Text, nullable=True)