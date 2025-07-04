import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.services.genre import GenreService
from app.models.genre import Genre

def test_create_genre_success(db_session: Session, sample_genre_data):
    """Test successful genre creation in service layer."""
    genre_service = GenreService()
    genre = Genre(**sample_genre_data)
    created_genre = genre_service.create(db_session, genre)
    
    assert created_genre.name == sample_genre_data["name"]
    assert created_genre.description == sample_genre_data["description"]
    assert created_genre.id is not None

def test_get_genre_by_id_success(db_session: Session, sample_genre_data):
    """Test getting genre by ID in service layer."""
    genre_service = GenreService()
    genre = Genre(**sample_genre_data)
    created_genre = genre_service.create(db_session, genre)
    
    retrieved_genre = genre_service.get_by_id(db_session, created_genre.id)
    assert retrieved_genre is not None
    assert retrieved_genre.name == sample_genre_data["name"]

def test_list_genres_success(db_session: Session, sample_genre_data):
    """Test listing all genres in service layer."""
    genre_service = GenreService()
    genre = Genre(**sample_genre_data)
    genre_service.create(db_session, genre)
    
    genres = genre_service.get_all(db_session)
    assert len(genres) >= 1
    assert any(genre.name == sample_genre_data["name"] for genre in genres)

def test_update_genre_success(db_session: Session, sample_genre_data):
    """Test updating genre in service layer."""
    genre_service = GenreService()
    genre = Genre(**sample_genre_data)
    created_genre = genre_service.create(db_session, genre)
    
    update_data = {"name": "Updated Action", "description": "Updated description"}
    updated_genre = genre_service.update(db_session, created_genre.id, update_data)
    
    assert updated_genre.name == "Updated Action"
    assert updated_genre.description == update_data["description"]

def test_delete_genre_success(db_session: Session, sample_genre_data):
    """Test deleting genre in service layer."""
    genre_service = GenreService()
    genre = Genre(**sample_genre_data)
    created_genre = genre_service.create(db_session, genre)
    
    genre_service.delete(db_session, created_genre.id)

    with pytest.raises(HTTPException) as exc_info:
        genre_service.get_by_id(db_session, created_genre.id)
    assert exc_info.value.status_code == 404

def test_get_genre_by_id_not_found(db_session: Session):
    """Test getting non-existent genre by ID raises HTTPException."""
    genre_service = GenreService()
    with pytest.raises(HTTPException) as exc_info:
        genre_service.get_by_id(db_session, 999)
    assert exc_info.value.status_code == 404
    assert "Genre with ID 999 not found" in str(exc_info.value.detail) 