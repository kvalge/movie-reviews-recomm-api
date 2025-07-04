from app.models.genre import Genre
from app.services.base_service import BaseEntityService


class GenreService(BaseEntityService[Genre]):
    def __init__(self):
        super().__init__(Genre)