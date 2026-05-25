"""
Shared pytest fixtures for the test suite.

Place here:
- Test database engine / session fixtures using an in-memory SQLite or test PostgreSQL DB
- A TestClient fixture wrapping app/main.py
- Fixtures that create test users (regular and admin) and return their JWT tokens
- A fixture that clears database tables between tests
"""
