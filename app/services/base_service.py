from abc import ABC
from typing import TypeVar, Generic, Type, List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.base_entity import BaseEntity

T = TypeVar('T', bound=BaseEntity)

class BaseService:
    def __init__(self, db: Session):
        self.db = db

class BaseEntityService(Generic[T], ABC):
    def __init__(self, model_class: Type[T], relationships: Optional[Dict[str, Dict[str, Any]]] = None):
        self.model_class = model_class
        self.relationships = relationships or {}
        
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

    def _handle_relationships_for_create(self, db: Session, entity: T, data: Dict[str, Any]) -> None:
        for rel_name, rel_config in self.relationships.items():
            field_name = rel_config['field_name']
            related_model = rel_config['model']
            relationship_attr = rel_config['relationship_attr']
            
            if field_name in data:
                related_ids = data[field_name]
                if related_ids:
                    related_entities = db.query(related_model).filter(related_model.id.in_(related_ids)).all()
                    setattr(entity, relationship_attr, related_entities)

    def _handle_relationships_for_update(self, db: Session, entity: T, update_data: Dict[str, Any]) -> None:
        for rel_name, rel_config in self.relationships.items():
            field_name = rel_config['field_name']
            related_model = rel_config['model']
            relationship_attr = rel_config['relationship_attr']
            
            if field_name in update_data:
                related_ids = update_data.pop(field_name)
                if related_ids is not None:
                    if related_ids:
                        related_entities = db.query(related_model).filter(related_model.id.in_(related_ids)).all()
                        setattr(entity, relationship_attr, related_entities)
                    else:
                        setattr(entity, relationship_attr, [])

    def create_entity_from_data(self, data: Dict[str, Any]) -> T:
        entity_data = data.copy()

        for rel_name, rel_config in self.relationships.items():
            field_name = rel_config['field_name']
            entity_data.pop(field_name, None)

        entity = self.model_class(**entity_data)

        for rel_name, rel_config in self.relationships.items():
            field_name = rel_config['field_name']
            if field_name in data and data[field_name] is not None:
                setattr(entity, f'_temp_{field_name}', data[field_name])
        
        return entity

    def create(self, db: Session, entity: T) -> T:
        temp_relationship_data = {}
        attrs_to_remove = []
        
        for rel_name, rel_config in self.relationships.items():
            field_name = rel_config['field_name']
            temp_attr = f'_temp_{field_name}'
            
            if hasattr(entity, temp_attr):
                temp_relationship_data[field_name] = getattr(entity, temp_attr)
                attrs_to_remove.append(temp_attr)

        for attr in attrs_to_remove:
            delattr(entity, attr)

        self._handle_relationships_for_create(db, entity, temp_relationship_data)
        
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

    def update(self, db: Session, id: int, update_data: Dict[str, Any]) -> T:
        entity = self.get_or_404(db, id)

        self._handle_relationships_for_update(db, entity, update_data)

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

