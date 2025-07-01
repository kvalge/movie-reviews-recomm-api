from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.position import Position
from app.schemas.position import PositionCreate, PositionUpdate, PositionOut
from app.services.position import create_position, get_position_by_id, update_position, delete_position, list_positions
from app.db.session import get_db

router = APIRouter(
    prefix="/api/positions",
    tags=["positions"]
)

@router.post("/", response_model=PositionOut, status_code=status.HTTP_201_CREATED)
def create_new_position(position: PositionCreate, db: Session = Depends(get_db)):
    existing = db.query(Position).filter(Position.name == position.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="position with this name already exists"
        )
    return create_position(db, position)

@router.get("/", response_model=List[PositionOut])
def get_all_positions(db: Session = Depends(get_db)):
    return list_positions(db)

@router.get("/{position_id}", response_model=PositionOut)
def get_position(position_id: int, db: Session = Depends(get_db)):
    return get_position_by_id(db, position_id)

@router.put("/{position_id}", response_model=PositionOut)
def update_existing_position(position_id: int, position_update: PositionUpdate, db: Session = Depends(get_db)):
    return update_position(db, position_id, position_update)

@router.delete("/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_position(position_id: int, db: Session = Depends(get_db)):
    delete_position(db, position_id)
    return None