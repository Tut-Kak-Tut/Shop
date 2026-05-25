"""
Tests for product and category endpoints.

Cover:
- GET /products returns paginated list with total and pages fields
- GET /products?search=sofa returns only matching products
- GET /products?category=sofas filters by category slug
- GET /products?min_price=500&max_price=1500 filters by price range
- GET /products?sort=price_asc returns products in ascending price order
- GET /products?page=2&limit=5 returns the correct page
- GET /products/{id} returns the correct product with nested category
- GET /products/999999 returns 404
- GET /products/categories returns list of all categories
"""
