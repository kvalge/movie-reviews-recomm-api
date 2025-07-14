from sqlalchemy import Column, String, Text, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.base_entity import BaseEntity
from app.db.session import Base

cast_and_crew_countries = Table(
    'cast_and_crew_countries',
    Base.metadata,
    Column('cast_and_crew_id', ForeignKey('cast_and_crew.id'), primary_key=True),
    Column('country_id', ForeignKey('countries.id'), primary_key=True)
)


class CastAndCrew(BaseEntity):
    __tablename__ = "cast_and_crew"

    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    stage_name = Column(String(256), nullable=True)
    birth_date = Column(Date, nullable=True)
    image_url = Column(String(2048), nullable=True)
    description = Column(Text, nullable=True)

    countries = relationship("Country", secondary=cast_and_crew_countries, back_populates="cast_and_crew")