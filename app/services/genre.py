from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate


def create_genre(db: Session, genre: GenreCreate) -> Genre:
    db_genre = Genre(
        name=genre.name,
        description=genre.description,
    )
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def get_genre_by_id(db: Session, genre_id: int) -> type[Genre]:
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )
    return genre


def list_genres(db: Session) -> list[type[Genre]]:
    return db.query(Genre).all()


def update_genre(db: Session, genre_id: int, updates: GenreUpdate) -> type[Genre]:
    genre = get_genre_by_id(db, genre_id)

    if updates.name is not None:
        genre.name = updates.name
    if updates.description is not None:
        genre.description = updates.description

    db.commit()
    db.refresh(genre)

    return genre


def delete_genre(db: Session, genre_id: int) -> None:
    genre = get_genre_by_id(db, genre_id)
    db.delete(genre)
    db.commit()
