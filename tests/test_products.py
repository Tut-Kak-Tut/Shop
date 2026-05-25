def test_get_products_paginated(client, test_product):
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "pages" in data
    assert len(data["items"]) >= 1

def test_get_products_search(client, test_product):
    response = client.get("/api/v1/products?search=sofa")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1
    
def test_get_products_by_category(client, test_product):
    response = client.get("/api/v1/products?category=sofas")
    assert response.status_code == 200
    assert response.json()["items"][0]["category"]["slug"] == "sofas"

def test_get_products_by_price_range(client, test_product):
    response = client.get("/api/v1/products?min_price=500&max_price=1500")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1

def test_get_products_sort_price_asc(client, test_product):
    response = client.get("/api/v1/products?sort=price_asc")
    assert response.status_code == 200

def test_get_products_pagination_limit(client, test_product):
    response = client.get("/api/v1/products?page=2&limit=5")
    assert response.status_code == 200
    assert response.json()["page"] == 2

def test_get_product_by_id(client, test_product):
    response = client.get(f"/api/v1/products/{test_product.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_product.id
    assert "category" in response.json()

def test_get_product_not_found(client):
    response = client.get("/api/v1/products/999999")
    assert response.status_code == 404

def test_get_categories(client, test_category):
    response = client.get("/api/v1/products/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)