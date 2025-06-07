from app.database import LaunchData, get_db, User
from datetime import datetime

def create_test_launch():
    db = next(get_db())
    test_launch = db.query(LaunchData).filter_by(id="test-launch-id").first()
    if not test_launch:
        test_launch = LaunchData(
            id="test-launch-id",
            name="Test Launch",
            flight_number=1,
            date_utc=datetime.fromisoformat("2023-01-01T00:00:00+00:00"),
            success=True,
            details="Test launch details",
            rocket_id="test-rocket"
        )
        db.add(test_launch)
        db.commit()
        db.refresh(test_launch)
    db.close()

def test_create_bookmark(client, auth_headers):
    create_test_launch()
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
    create_test_launch()
    # Create the bookmark first
    client.post(
        "/bookmarks/",
        headers=auth_headers,
        json={"launch_id": "test-launch-id"}
    )
    # Try to create it again (should be duplicate)
    response = client.post(
        "/bookmarks/",
        headers=auth_headers,
        json={"launch_id": "test-launch-id"}
    )
    assert response.status_code == 400  # Bad request for duplicate bookmark

def test_delete_bookmark(client, auth_headers):
    create_test_launch()
    # Create the bookmark to delete
    client.post(
        "/bookmarks/",
        headers=auth_headers,
        json={"launch_id": "test-launch-id"}
    )
    response = client.delete(
        f"/bookmarks/test-launch-id",
        headers=auth_headers
    )
    assert response.status_code == 204  # No content on successful delete
