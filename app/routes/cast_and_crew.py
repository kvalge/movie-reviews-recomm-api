from app.schemas.cast_and_crew import CastAndCrewCreate, CastAndCrewUpdate, CastAndCrewOut
from app.services.cast_and_crew import CastAndCrewService
from app.routes.base_routes import BaseRouter

cast_and_crew_service = CastAndCrewService()

router = BaseRouter(
    service=cast_and_crew_service,
    schema_create=CastAndCrewCreate,
    schema_update=CastAndCrewUpdate,
    schema_out=CastAndCrewOut,
    prefix="cast_and_crew",
    tags=["CastAndCrew"]
).router
