from app.core.security import create_access_token

def test_register_success(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "new@example.com", "password": "Password123!", "first_name": "John", "last_name": "Doe"
    })
    assert response.status_code == 201
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

def test_register_duplicate_email(client, test_user):
    response = client.post("/api/v1/auth/register", json={
        "email": test_user.email, "password": "Password123!", "first_name": "John", "last_name": "Doe"
    })
    assert response.status_code == 400

def test_register_short_password(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "fail@example.com", "password": "short", "first_name": "John", "last_name": "Doe"
    })
    assert response.status_code == 422

def test_login_valid_credentials(client, test_user):
    response = client.post("/api/v1/auth/login", json={"email": test_user.email, "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client, test_user):
    response = client.post("/api/v1/auth/login", json={"email": test_user.email, "password": "wrong"})
    assert response.status_code == 401

def test_login_unknown_email(client):
    response = client.post("/api/v1/auth/login", json={"email": "unknown@example.com", "password": "password123"})
    assert response.status_code == 401

def test_refresh_valid_token(client, test_user):
    login = client.post("/api/v1/auth/login", json={"email": test_user.email, "password": "password123"})
    refresh_token = login.json()["refresh_token"]
    response = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_refresh_with_access_token(client, test_user):
    access_token = create_access_token(test_user.email)
    response = client.post("/api/v1/auth/refresh", json={"refresh_token": access_token})
    assert response.status_code == 401

def test_refresh_expired_or_malformed(client):
    response = client.post("/api/v1/auth/refresh", json={"refresh_token": "malformed.token.string"})
    assert response.status_code == 401