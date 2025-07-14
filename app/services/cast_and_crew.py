from app.models.cast_and_crew import CastAndCrew
from app.models.country import Country
from app.services.base_service import BaseEntityService


class CastAndCrewService(BaseEntityService[CastAndCrew]):
    def __init__(self):
        super().__init__(CastAndCrew, relationships={
            'countries': {
                'model': Country,
                'field_name': 'country_ids',
                'relationship_attr': 'countries'
            }
        })