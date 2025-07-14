from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base_entity import BaseEntity


class Country(BaseEntity):
    __tablename__ = "countries"

    code = Column(String(2), unique=True, nullable=False, index=True) # ISO 3166-1 alpha-2 code
    name = Column(String(100), nullable=False)

    cast_and_crew = relationship("CastAndCrew", secondary="cast_and_crew_countries", back_populates="countries")

    def __repr__(self):
        return f"<Country(code='{self.code}', name='{self.name}')>" 