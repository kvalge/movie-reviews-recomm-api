from app.models.position import Position
from app.services.base_service import BaseEntityService


class PositionService(BaseEntityService[Position]):
    def __init__(self):
        super().__init__(Position)

