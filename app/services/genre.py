from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate
from app.services.base_service import BaseEntityService


class GenreService(BaseEntityService[Genre]):
    def __init__(self):
        super().__init__(Genre)


# Standalone functions for backward compatibility with tests
def create_genre(db: Session, genre: GenreCreate) -> Genre:
    """Create a new genre."""
    try:
        db_genre = Genre(name=genre.name, description=genre.description)
        db.add(db_genre)
        db.commit()
        db.refresh(db_genre)
        return db_genre
    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint failed" in str(e) or "duplicate key value" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A genre with this name already exists"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database constraint violation"
            )


def get_genre_by_id(db: Session, genre_id: int) -> Genre:
    """Get a genre by ID, raise HTTPException if not found."""
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )
    return genre


def list_genres(db: Session) -> List[Genre]:
    """Get all genres."""
    return db.query(Genre).all()


def update_genre(db: Session, genre_id: int, genre_update: GenreUpdate) -> Genre:
    """Update a genre."""
    genre = get_genre_by_id(db, genre_id)  # This will raise HTTPException if not found
    
    update_data = genre_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(genre, key, value)
    
    db.commit()
    db.refresh(genre)
    return genre


def delete_genre(db: Session, genre_id: int) -> None:
    """Delete a genre."""
    genre = get_genre_by_id(db, genre_id)  # This will raise HTTPException if not found
    db.delete(genre)
    db.commit()
