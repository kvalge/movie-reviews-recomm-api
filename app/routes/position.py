from app.schemas.position import PositionCreate, PositionUpdate, PositionOut
from app.services.position import PositionService
from app.routes.base_routes import BaseRouter

genre_service = PositionService()

router = BaseRouter(
    service=genre_service,
    schema_create=PositionCreate,
    schema_update=PositionUpdate,
    schema_out=PositionOut,
    prefix="position",
    tags=["Positions"]
).router
