from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreOut, GenreUpdate
from app.services.genre import create_genre, get_genre_by_id, update_genre, delete_genre, list_genres
from app.db.session import get_db

router = APIRouter(
    prefix="/api/genres",
    tags=["genres"]
)

@router.post("/", response_model=GenreOut, status_code=status.HTTP_201_CREATED)
def create_new_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    existing = db.query(Genre).filter(Genre.name == genre.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Genre with this name already exists"
        )
    return create_genre(db, genre)

@router.get("/", response_model=List[GenreOut])
def get_all_genres(db: Session = Depends(get_db)):
    return list_genres(db)  # you need to implement list_genres service function

@router.get("/{genre_id}", response_model=GenreOut)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    return get_genre_by_id(db, genre_id)

@router.put("/{genre_id}", response_model=GenreOut)
def update_existing_genre(genre_id: int, genre_update: GenreUpdate, db: Session = Depends(get_db)):
    return update_genre(db, genre_id, genre_update)

@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_genre(genre_id: int, db: Session = Depends(get_db)):
    delete_genre(db, genre_id)
    return None
