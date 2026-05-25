def test_get_cart_without_token(client):
    response = client.get("/api/v1/cart")
    assert response.status_code == 401

def test_get_cart_new_user(client, test_user_token):
    response = client.get("/api/v1/cart", headers={"Authorization": f"Bearer {test_user_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert float(data["total_price"]) == 0.0

def test_add_product_to_cart(client, test_user_token, test_product):
    response = client.post(
        "/api/v1/cart/items",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={"product_id": test_product.id, "quantity": 2}
    )
    assert response.status_code == 201
    assert response.json()["total_items"] == 2

def test_add_same_product_increments(client, test_user_token, test_product):
    client.post("/api/v1/cart/items", headers={"Authorization": f"Bearer {test_user_token}"}, json={"product_id": test_product.id, "quantity": 1})
    response = client.post("/api/v1/cart/items", headers={"Authorization": f"Bearer {test_user_token}"}, json={"product_id": test_product.id, "quantity": 2})
    assert response.status_code == 201
    assert response.json()["total_items"] == 3

def test_add_non_existent_product(client, test_user_token):
    response = client.post("/api/v1/cart/items", headers={"Authorization": f"Bearer {test_user_token}"}, json={"product_id": 999, "quantity": 1})
    assert response.status_code == 404

def test_update_item_quantity(client, test_user_token, test_product):
    client.post("/api/v1/cart/items", headers={"Authorization": f"Bearer {test_user_token}"}, json={"product_id": test_product.id, "quantity": 1})
    response = client.put(f"/api/v1/cart/items/{test_product.id}", headers={"Authorization": f"Bearer {test_user_token}"}, json={"quantity": 5})
    assert response.status_code == 200
    assert response.json()["items"][0]["quantity"] == 5

def test_update_item_quantity_less_than_one(client, test_user_token, test_product):
    client.post("/api/v1/cart/items", headers={"Authorization": f"Bearer {test_user_token}"}, json={"product_id": test_product.id, "quantity": 1})
    response = client.put(f"/api/v1/cart/items/{test_product.id}", headers={"Authorization": f"Bearer {test_user_token}"}, json={"quantity": 0})
    assert response.status_code == 400

def test_update_item_not_in_cart(client, test_user_token):
    response = client.put("/api/v1/cart/items/999", headers={"Authorization": f"Bearer {test_user_token}"}, json={"quantity": 2})
    assert response.status_code == 404

def test_remove_item(client, test_user_token, test_product):
    client.post("/api/v1/cart/items", headers={"Authorization": f"Bearer {test_user_token}"}, json={"product_id": test_product.id, "quantity": 1})
    response = client.delete(f"/api/v1/cart/items/{test_product.id}", headers={"Authorization": f"Bearer {test_user_token}"})
    assert response.status_code == 200
    assert response.json()["total_items"] == 0

def test_remove_item_not_in_cart(client, test_user_token):
    response = client.delete("/api/v1/cart/items/999", headers={"Authorization": f"Bearer {test_user_token}"})
    assert response.status_code == 404

def test_clear_all_items(client, test_user_token, test_product):
    client.post("/api/v1/cart/items", headers={"Authorization": f"Bearer {test_user_token}"}, json={"product_id": test_product.id, "quantity": 1})
    response = client.delete("/api/v1/cart", headers={"Authorization": f"Bearer {test_user_token}"})
    assert response.status_code == 204

def test_cart_total_price(client, test_user_token, test_product):
    response = client.post("/api/v1/cart/items", headers={"Authorization": f"Bearer {test_user_token}"}, json={"product_id": test_product.id, "quantity": 3})
    expected_price = test_product.price * 3
    assert float(response.json()["total_price"]) == float(expected_price)