from app.schemas.position import PositionCreate, PositionUpdate, PositionOut
from app.services.position import PositionService
from app.routes.base_routes import BaseRouter

position_service = PositionService()

router = BaseRouter(
    service=position_service,
    schema_create=PositionCreate,
    schema_update=PositionUpdate,
    schema_out=PositionOut,
    prefix="positions",
    tags=["Positions"]
).router
