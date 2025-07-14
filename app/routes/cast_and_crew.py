from fastapi import Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.cast_and_crew import CastAndCrewCreate, CastAndCrewUpdate, CastAndCrewOut
from app.services.cast_and_crew import CastAndCrewService
from app.routes.base_routes import BaseRouter

cast_and_crew_service = CastAndCrewService()

class CastAndCrewRouter(BaseRouter):
    def _add_routes(self):
        super()._add_routes()

        routes_to_remove = []
        for route in self.router.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                if 'POST' in route.methods and route.path == '/api/cast_and_crew/' and route.endpoint.__name__ == 'create':
                    routes_to_remove.append(route)
        
        for route in routes_to_remove:
            self.router.routes.remove(route)

        @self.router.post("/", response_model=self.schema_out, status_code=status.HTTP_201_CREATED)
        def create(entity_data: CastAndCrewCreate, db: Session = Depends(get_db)):
            entity = cast_and_crew_service.create_entity_from_data(entity_data.model_dump())
            return cast_and_crew_service.create(db, entity)

router = CastAndCrewRouter(
    service=cast_and_crew_service,
    schema_create=CastAndCrewCreate,
    schema_update=CastAndCrewUpdate,
    schema_out=CastAndCrewOut,
    prefix="cast_and_crew",
    tags=["CastAndCrew"]
).router
