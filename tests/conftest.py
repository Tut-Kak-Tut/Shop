import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.api.deps import get_db
from app.models.user import User
from app.models.product import Category, Product
from app.core.security import get_password_hash, create_access_token, create_refresh_token

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db):
    user = User(
        email="user@example.com",
        hashed_password=get_password_hash("password123"),
        first_name="Test",
        last_name="User",
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="function")
def test_user_token(test_user):
    return create_access_token(subject=test_user.email)

@pytest.fixture(scope="function")
def test_category(db):
    category = Category(name="Sofas", slug="sofas")
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@pytest.fixture(scope="function")
def test_product(db, test_category):
    product = Product(
        name="Leather Sofa",
        description="Premium leather sofa",
        price=1000.00,
        stock=5,
        category_id=test_category.id,
        material="Leather",
        color="Black"
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product