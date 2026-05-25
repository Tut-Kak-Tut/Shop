def test_get_profile_without_token(client):
    response = client.get("/api/v1/profile")
    assert response.status_code == 401

def test_get_profile_with_token(client, test_user_token, test_user):
    response = client.get("/api/v1/profile", headers={"Authorization": f"Bearer {test_user_token}"})
    assert response.status_code == 200
    assert response.json()["email"] == test_user.email

def test_update_profile_all_fields(client, test_user_token):
    response = client.put(
        "/api/v1/profile",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={"first_name": "New", "last_name": "Name", "phone": "123456789", "address": "Test Street"}
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "New"
    assert response.json()["phone"] == "123456789"

def test_update_profile_partial(client, test_user_token):
    response = client.put(
        "/api/v1/profile",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={"first_name": "Partial"}
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "Partial"

def test_update_password_correct_current(client, test_user_token):
    response = client.put(
        "/api/v1/profile/password",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={"current_password": "password123", "new_password": "NewPassword123!"}
    )
    assert response.status_code == 204

def test_update_password_wrong_current(client, test_user_token):
    response = client.put(
        "/api/v1/profile/password",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={"current_password": "wrong", "new_password": "NewPassword123!"}
    )
    assert response.status_code == 400

def test_update_password_too_short(client, test_user_token):
    response = client.put(
        "/api/v1/profile/password",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={"current_password": "password123", "new_password": "short"}
    )
    assert response.status_code == 422