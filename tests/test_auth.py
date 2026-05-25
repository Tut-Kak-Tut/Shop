"""
Tests for authentication endpoints: POST /api/v1/auth/register, /login, /refresh.

Cover:
- Successful registration returns 201 with access and refresh tokens
- Registration with a duplicate email returns 400
- Registration with a short password returns 422
- Login with valid credentials returns 200 with tokens
- Login with wrong password returns 401
- Login with unknown email returns 401
- Refresh with a valid refresh token returns a new token pair
- Refresh with an access token (wrong type) returns 401
- Refresh with an expired or malformed token returns 401
"""
