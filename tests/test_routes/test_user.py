from fastapi import status

def test_create_user_success(client, sample_user_data):
    """Test successful user creation."""
    response = client.post("/api/users/", json=sample_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == sample_user_data["email"]
    assert data["username"] == sample_user_data["username"]
    assert "password" not in data

def test_create_user_duplicate_email(client, sample_user_data):
    """Test user creation with duplicate email fails."""
    client.post("/api/users/", json=sample_user_data)

    duplicate_data = sample_user_data.copy()
    duplicate_data["username"] = "differentuser"
    response = client.post("/api/users/", json=duplicate_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_get_user_by_id(client, sample_user_data):
    """Test getting user by ID."""
    create_response = client.post("/api/users/", json=sample_user_data)
    user_id = create_response.json()["id"]

    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == sample_user_data["email"]

def test_get_user_not_found(client):
    """Test getting non-existent user returns 404."""
    response = client.get("/api/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND 