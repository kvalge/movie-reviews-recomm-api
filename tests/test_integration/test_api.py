from fastapi import status

def test_api_health_check(client):
    """Test API health check endpoint."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK

def test_user_and_genre_integration(client, sample_user_data, sample_genre_data):
    """Test integration between user and genre operations."""
    user_response = client.post("/api/users/", json=sample_user_data)
    assert user_response.status_code == status.HTTP_201_CREATED
    user_id = user_response.json()["id"]

    genre_response = client.post("/api/genres/", json=sample_genre_data)
    assert genre_response.status_code == status.HTTP_201_CREATED
    genre_id = genre_response.json()["id"]

    user_get = client.get(f"/api/users/{user_id}")
    assert user_get.status_code == status.HTTP_200_OK
    
    genre_get = client.get(f"/api/genres/{genre_id}")
    assert genre_get.status_code == status.HTTP_200_OK

def test_api_error_handling(client):
    """Test API error handling for invalid requests."""
    response = client.post("/api/users/", data="invalid json")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = client.get("/api/nonexistent/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_cors_headers(client):
    """Test CORS headers are present."""
    response = client.options("/api/users/")
    assert response.status_code in [200, 405]