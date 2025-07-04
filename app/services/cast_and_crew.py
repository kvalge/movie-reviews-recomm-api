from app.models.cast_and_crew import CastAndCrew
from app.services.base_service import BaseEntityService


class CastAndCrewService(BaseEntityService[CastAndCrew]):
    def __init__(self):
        super().__init__(CastAndCrew)