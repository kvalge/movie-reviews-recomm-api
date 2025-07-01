from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.position import Position
from app.schemas.position import PositionCreate, PositionUpdate


def create_position(db: Session, position: PositionCreate) -> Position:
    db_position = Position(
        name=position.name.capitalize(),
        description=position.description,
    )
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position  # type: ignore


def get_position_by_id(db: Session, position_id: int) -> Position:
    position: Optional[Position] = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found"
        )
    return position  # type: ignore


def list_positions(db: Session) -> List[Position]:
    return db.query(Position).all()  # type: ignore


def update_position(db: Session, position_id: int, updates: PositionUpdate) -> Position:
    position: Position = get_position_by_id(db, position_id)

    if updates.name is not None:
        position.name = updates.name.capitalize()
    if updates.description is not None:
        position.description = updates.description

    db.commit()
    db.refresh(position)

    return position  # type: ignore


def delete_position(db: Session, position_id: int) -> None:
    position: Position = get_position_by_id(db, position_id)
    db.delete(position)
    db.commit()
