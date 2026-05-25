"""
Tests for profile endpoints (all require authentication).

Cover:
- GET /profile without token returns 401
- GET /profile with valid token returns user data matching the registered email
- PUT /profile updates first_name, last_name, phone, address
- PUT /profile with a partial body (only one field) only updates that field
- PUT /profile/password with correct current_password returns 204
- PUT /profile/password with wrong current_password returns 400
- PUT /profile/password with new password < 8 chars returns 422
"""
