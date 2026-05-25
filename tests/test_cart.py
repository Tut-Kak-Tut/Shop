"""
Tests for cart endpoints (all require authentication).

Cover:
- GET /cart without token returns 401
- GET /cart returns empty cart for a new user (items=[], total_price=0)
- POST /cart/items adds a product and returns updated cart
- POST /cart/items with the same product_id increments quantity
- POST /cart/items with a non-existent product_id returns 404
- PUT /cart/items/{product_id} sets the quantity to the given value
- PUT /cart/items/{product_id} with quantity < 1 returns 400
- PUT /cart/items/{product_id} for an item not in cart returns 404
- DELETE /cart/items/{product_id} removes item and returns updated cart
- DELETE /cart/items/{product_id} for an item not in cart returns 404
- DELETE /cart clears all items and returns 204
- cart total_price is the correct sum of (price * quantity) across all items
"""
