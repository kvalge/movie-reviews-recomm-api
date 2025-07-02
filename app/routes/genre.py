from app.schemas.genre import GenreCreate, GenreUpdate, GenreOut
from app.services.genre import GenreService
from app.routes.base_routes import BaseRouter

genre_service = GenreService()

router = BaseRouter(
    service=genre_service,
    schema_create=GenreCreate,
    schema_update=GenreUpdate,
    schema_out=GenreOut,
    prefix="genres",
    tags=["Genres"]
).router
