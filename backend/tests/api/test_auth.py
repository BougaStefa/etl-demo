def test_register_success(client):
    """Test successful user registration"""
    response = client.post("/register", json={
        "username": "testuser1",
        "password": "TestPassword123!",
        "email": "testuser1@example.com"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser1"
    assert "id" in data

def test_register_duplicate_username(client):
    """Test registering the same username twice fails"""
    client.post("/register", json={
        "username": "testuser2",
        "password": "TestPassword123!",
        "email": "testuser2@example.com"
    })
    response = client.post("/register", json={
        "username": "testuser2",
        "password": "AnotherPassword!",
        "email": "testuser2b@example.com"
    })
    assert response.status_code == 400

def test_login_success(client):
    """Test successful login after registering"""
    client.post("/register", json={
        "username": "loginuser",
        "password": "MySecretPassword456",
        "email": "loginuser@example.com"
    })
    response = client.post("/token", data={
        "username": "loginuser",
        "password": "MySecretPassword456"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_login_wrong_password(client):
    """Test login fails with wrong password"""
    client.post("/register", json={
        "username": "wrongpassuser",
        "password": "GoodPassword!",
        "email": "wrongpassuser@example.com"
    })
    response = client.post("/token", data={
        "username": "wrongpassuser",
        "password": "BadPassword!"
    })
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    """Test login fails with non-existent user"""
    response = client.post("/token", data={
        "username": "nosuchuser",
        "password": "anything"
    })
    assert response.status_code == 401
