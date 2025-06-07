from app.database import  LaunchData, get_db

def test_create_bookmark_unauthorized(client):
    """Test unauthorized access to bookmark creation"""
    response = client.post("/bookmarks/", json={"launch_id": "test-launch"})
    assert response.status_code == 401  # request rejected without token

def test_create_bookmark(client, auth_headers):
    """Test creating a bookmark"""
    # First create a test launch in the database
    db = next(get_db())
    test_launch = LaunchData(
        id="test-launch-id",
        name="Test Launch",
        flight_number=1,
        date_utc="2023-01-01T00:00:00Z",
        success=True,
        details="Test launch details",
        rocket_id="test-rocket"
    )
    db.add(test_launch)
    db.commit()

    # Try to create a bookmark
    response = client.post(
        "/bookmarks/",
        headers=auth_headers,
        json={"launch_id": "test-launch-id"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["launch_id"] == "test-launch-id"
    assert "created_at" in data
    assert data["created_at"] is not None

def test_create_duplicate_bookmark(client, auth_headers):
    """Test attempting to create a duplicate bookmark"""
    response = client.post(
        "/bookmarks/",
        headers=auth_headers,
        json={"launch_id": "test-launch-id"}
    )
    assert response.status_code == 400  # Bad request for duplicate bookmark

def test_create_bookmark_nonexistent_launch(client, auth_headers):
    """Test creating a bookmark for a non-existent launch"""
    response = client.post(
        "/bookmarks/",
        headers=auth_headers,
        json={"launch_id": "nonexistent-launch"}
    )
    assert response.status_code == 404  # Not found

def test_get_bookmarks(client, auth_headers):
    """Test getting user's bookmarks"""
    response = client.get("/bookmarks/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "launch_id" in data[0]
        assert "created_at" in data[0]

def test_delete_bookmark(client, auth_headers):
    """Test deleting a bookmark"""
    # Try to delete the test bookmark we created
    response = client.delete(
        f"/bookmarks/test-launch-id",
        headers=auth_headers
    )
    assert response.status_code == 204  # No content on successful delete

def test_delete_nonexistent_bookmark(client, auth_headers):
    """Test deleting a non-existent bookmark"""
    response = client.delete(
        f"/bookmarks/nonexistent-launch",
        headers=auth_headers
    )
    assert response.status_code == 404  # Not found
