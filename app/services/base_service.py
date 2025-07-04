from abc import ABC
from typing import TypeVar, Generic, Type, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.base_entity import BaseEntity

T = TypeVar('T', bound=BaseEntity)

class BaseEntityService(Generic[T], ABC):
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class

    def get_all(self, db: Session) -> List[T]:
        return db.query(self.model_class).all()

    def get_or_404(self, db: Session, id: int) -> T:
        entity = db.query(self.model_class).filter(self.model_class.id == id).first() # type: ignore
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model_class.__name__} with ID {id} not found"
            )
        return entity

    def get_by_id(self, db: Session, id: int) -> T:
        return self.get_or_404(db, id)

    def create(self, db: Session, entity: T) -> T:
        try:
            db.add(entity)
            db.commit()
            db.refresh(entity)
            return entity
        except IntegrityError as e:
            db.rollback()
            if "UNIQUE constraint failed" in str(e) or "duplicate key value" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"A {self.model_class.__name__.lower()} with this data already exists"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Database constraint violation"
                )

    def update(self, db: Session, id: int, update_data: dict) -> T:
        entity = self.get_or_404(db, id)
        for key, value in update_data.items():
            setattr(entity, key, value)
        db.commit()
        db.refresh(entity)
        return entity

    def delete(self, db: Session, id: int) -> bool:
        entity = self.get_or_404(db, id)
        db.delete(entity)
        db.commit()
        return True

