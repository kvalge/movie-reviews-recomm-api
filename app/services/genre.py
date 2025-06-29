from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate


def create_genre(db: Session, genre: GenreCreate) -> Genre:
    db_genre = Genre(
        name=genre.name.capitalize(),
        description=genre.description,
    )
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre  # type: ignore


def get_genre_by_id(db: Session, genre_id: int) -> Genre:
    genre: Optional[Genre] = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )
    return genre  # type: ignore


def list_genres(db: Session) -> List[Genre]:
    return db.query(Genre).all()  # type: ignore


def update_genre(db: Session, genre_id: int, updates: GenreUpdate) -> Genre:
    genre: Genre = get_genre_by_id(db, genre_id)

    if updates.name is not None:
        genre.name = updates.name.capitalize()
    if updates.description is not None:
        genre.description = updates.description

    db.commit()
    db.refresh(genre)

    return genre  # type: ignore


def delete_genre(db: Session, genre_id: int) -> None:
    genre: Genre = get_genre_by_id(db, genre_id)
    db.delete(genre)
    db.commit()
