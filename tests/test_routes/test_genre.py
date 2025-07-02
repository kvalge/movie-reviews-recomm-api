from fastapi import status

def test_create_genre_success(client, sample_genre_data):
    """Test successful genre creation."""
    response = client.post("/api/genres/", json=sample_genre_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == sample_genre_data["name"]
    assert data["description"] == sample_genre_data["description"]

def test_create_genre_duplicate_name(client, sample_genre_data):
    """Test genre creation with duplicate name fails."""
    client.post("/api/genres/", json=sample_genre_data)

    duplicate_data = sample_genre_data.copy()
    duplicate_data["description"] = "Different description"
    response = client.post("/api/genres/", json=duplicate_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_get_all_genres(client, sample_genre_data):
    """Test getting all genres."""
    client.post("/api/genres/", json=sample_genre_data)

    response = client.get("/api/genres/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    assert any(genre["name"] == sample_genre_data["name"] for genre in data)

def test_get_genre_by_id(client, sample_genre_data):
    """Test getting genre by ID."""
    create_response = client.post("/api/genres/", json=sample_genre_data)
    genre_id = create_response.json()["id"]

    response = client.get(f"/api/genres/{genre_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == sample_genre_data["name"]

def test_update_genre(client, sample_genre_data):
    """Test updating genre."""
    create_response = client.post("/api/genres/", json=sample_genre_data)
    genre_id = create_response.json()["id"]

    update_data = {"name": "Updated Action", "description": "Updated description"}
    response = client.put(f"/api/genres/{genre_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Action"

def test_delete_genre(client, sample_genre_data):
    """Test deleting genre."""
    create_response = client.post("/api/genres/", json=sample_genre_data)
    genre_id = create_response.json()["id"]

    response = client.delete(f"/api/genres/{genre_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/api/genres/{genre_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND 