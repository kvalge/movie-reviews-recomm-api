import pycountry
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.country import Country
from app.schemas.country import CountryOut


class CountryService:
    def __init__(self, db: Session):
        self.db = db

    def populate_countries(self) -> None:
        if self.db.query(Country).count() > 0:
            return

        countries_data = []
        for country in pycountry.countries:
            countries_data.append(Country(
                code=country.alpha_2,
                name=country.name
            ))

        self.db.bulk_save_objects(countries_data)
        self.db.commit()

    def get_all_countries(self) -> List[CountryOut]:
        self.populate_countries()
        
        countries = self.db.query(Country).order_by(Country.name).all()
        return [CountryOut.model_validate(country) for country in countries]

    def get_country_by_id(self, country_id: int) -> Optional[CountryOut]:
        country = self.db.query(Country).filter(Country.id == country_id).first()
        if country:
            return CountryOut.model_validate(country)
        return None

    def get_countries_by_ids(self, country_ids: List[int]) -> List[CountryOut]:
        countries = self.db.query(Country).filter(Country.id.in_(country_ids)).all()
        return [CountryOut.model_validate(country) for country in countries] 