import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.services.genre import create_genre, get_genre_by_id, list_genres, update_genre, delete_genre
from app.schemas.genre import GenreCreate, GenreUpdate

def test_create_genre_success(db_session: Session, sample_genre_data):
    """Test successful genre creation in service layer."""
    genre_create = GenreCreate(**sample_genre_data)
    genre = create_genre(db_session, genre_create)
    
    assert genre.name == sample_genre_data["name"]
    assert genre.description == sample_genre_data["description"]
    assert genre.id is not None

def test_get_genre_by_id_success(db_session: Session, sample_genre_data):
    """Test getting genre by ID in service layer."""
    genre_create = GenreCreate(**sample_genre_data)
    created_genre = create_genre(db_session, genre_create)
    
    retrieved_genre = get_genre_by_id(db_session, created_genre.id)
    assert retrieved_genre is not None
    assert retrieved_genre.name == sample_genre_data["name"]

def test_list_genres_success(db_session: Session, sample_genre_data):
    """Test listing all genres in service layer."""
    genre_create = GenreCreate(**sample_genre_data)
    create_genre(db_session, genre_create)
    
    genres = list_genres(db_session)
    assert len(genres) >= 1
    assert any(genre.name == sample_genre_data["name"] for genre in genres)

def test_update_genre_success(db_session: Session, sample_genre_data):
    """Test updating genre in service layer."""
    genre_create = GenreCreate(**sample_genre_data)
    created_genre = create_genre(db_session, genre_create)
    
    update_data = {"name": "Updated Action", "description": "Updated description"}
    genre_update = GenreUpdate(**update_data)
    updated_genre = update_genre(db_session, created_genre.id, genre_update)
    
    assert updated_genre.name == "Updated Action"
    assert updated_genre.description == update_data["description"]

def test_delete_genre_success(db_session: Session, sample_genre_data):
    """Test deleting genre in service layer."""
    genre_create = GenreCreate(**sample_genre_data)
    created_genre = create_genre(db_session, genre_create)
    
    delete_genre(db_session, created_genre.id)

    with pytest.raises(HTTPException) as exc_info:
        get_genre_by_id(db_session, created_genre.id)
    assert exc_info.value.status_code == 404

def test_get_genre_by_id_not_found(db_session: Session):
    """Test getting non-existent genre by ID raises HTTPException."""
    with pytest.raises(HTTPException) as exc_info:
        get_genre_by_id(db_session, 999)
    assert exc_info.value.status_code == 404
    assert "Genre not found" in str(exc_info.value.detail) 