from typing import TypeVar, Generic, Type, cast, List
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.base_service import BaseEntityService

TCreate = TypeVar("TCreate", bound=BaseModel)
TUpdate = TypeVar("TUpdate", bound=BaseModel)
TOut = TypeVar("TOut", bound=BaseModel)


class BaseRouter(Generic[TCreate, TUpdate, TOut]):
    def __init__(
        self,
        service: BaseEntityService,
        schema_create: Type[TCreate],
        schema_update: Type[TUpdate],
        schema_out: Type[TOut],
        prefix: str,
        tags: List[str],
    ):
        self.service = service
        self.schema_create = schema_create
        self.schema_update = schema_update
        self.schema_out = schema_out
        self.router = APIRouter(prefix=f"/api/{prefix}", tags=tags)

        self._add_routes()

    def _add_routes(self):
        schema_create_type = cast(Type[TCreate], self.schema_create)
        schema_update_type = cast(Type[TUpdate], self.schema_update)

        @self.router.get("/", response_model=List[self.schema_out])
        def get_all(db: Session = Depends(get_db)):
            return self.service.get_all(db)

        @self.router.get("/{id}", response_model=self.schema_out)
        def get_by_id(id: int, db: Session = Depends(get_db)):
            return self.service.get_by_id(db, id)

        @self.router.post("/", response_model=self.schema_out, status_code=status.HTTP_201_CREATED)
        def create(entity_data: schema_create_type, db: Session = Depends(get_db)):
            entity = self.service.model_class(**entity_data.model_dump())
            return self.service.create(db, entity)

        @self.router.put("/{id}", response_model=self.schema_out)
        def update(id: int, entity_data: schema_update_type, db: Session = Depends(get_db)):
            return self.service.update(db, id, entity_data.model_dump(exclude_unset=True))

        @self.router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
        def delete(id: int, db: Session = Depends(get_db)):
            success = self.service.delete(db, id)
            if not success:
                raise HTTPException(status_code=404, detail="Entity not found")
            return None
