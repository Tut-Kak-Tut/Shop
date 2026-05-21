# FurniShop — Online Furniture Store

A full-featured online furniture store built with **Python FastAPI**, **PostgreSQL**, and **Docker**. The application includes a REST API backend, a vanilla HTML/JS frontend, and a basic admin panel — all served from a single container.

---

## Features

- **Product Catalog** — Browse furniture with search, multi-criteria filters (category, price range, material, color), and sorting
- **User Accounts** — Register and log in with email/password; JWT-based authentication (access + refresh tokens)
- **Customer Profile** — View and edit personal info (name, email, phone, shipping address) and change password
- **Shopping Cart** — Add items, adjust quantities, remove individual items, clear entire cart; total price computed server-side
- **Admin Panel** — Create, edit, and delete products and categories (admin users only)
- **Interactive API Docs** — Swagger UI at `/docs` and ReDoc at `/redoc`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI 0.115 |
| ORM | SQLAlchemy 2.0 (sync), Alembic migrations |
| Database | PostgreSQL 16 |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Validation | Pydantic v2 |
| Frontend | Vanilla HTML5 / CSS3 / JavaScript (ES6+) |
| Containerization | Docker, Docker Compose v2 |

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) >= 24.0
- [Docker Compose](https://docs.docker.com/compose/) >= 2.20 (included with Docker Desktop)

No Python or Node.js installation required on the host machine.

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Tut-Kak-Tut/Shop.git
cd Shop

# 2. Copy and configure environment variables
cp .env.example .env
# Edit .env and set a strong SECRET_KEY before deploying to production

# 3. Build and start all services
docker compose up --build
```

The API is available at **http://localhost:8000**
The shop frontend opens automatically at **http://localhost:8000**
Interactive API docs: **http://localhost:8000/docs**

### Seed demo data

After the containers are running, populate the database with 15 sample products, 5 categories, and two demo accounts:

```bash
docker compose exec api python -m scripts.seed_data
```

Demo credentials:

| Role | Email | Password |
|---|---|---|
| Regular user | demo@example.com | password123 |
| Admin | admin@example.com | admin123 |

---

## Environment Variables

Copy `.env.example` to `.env` and adjust values as needed.

| Variable | Description | Default in example |
|---|---|---|
| `POSTGRES_USER` | PostgreSQL username | `shopuser` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `shoppassword` |
| `POSTGRES_DB` | PostgreSQL database name | `shopdb` |
| `POSTGRES_HOST` | DB host (Docker service name) | `db` |
| `POSTGRES_PORT` | DB port | `5432` |
| `DATABASE_URL` | Full SQLAlchemy connection string | *(assembled from above)* |
| `SECRET_KEY` | JWT signing secret — **change this!** | placeholder |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token TTL | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token TTL | `7` |
| `BACKEND_CORS_ORIGINS` | JSON array of allowed CORS origins | `["http://localhost:8000"]` |

---

## API Reference

All endpoints are prefixed with `/api/v1`.

### Authentication

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/register` | -- | Register a new user, returns token pair |
| `POST` | `/auth/login` | -- | Login with email/password, returns token pair |
| `POST` | `/auth/refresh` | -- | Exchange a refresh token for a new token pair |

### Products

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/products` | -- | List products with optional filters (see below) |
| `GET` | `/products/{id}` | -- | Get single product by ID |
| `GET` | `/products/categories` | -- | List all categories |

**Query parameters for `GET /products`:**

| Parameter | Type | Description |
|---|---|---|
| `search` | string | Full-text search across name and description |
| `category` | string | Filter by category slug (e.g. `sofas`) |
| `min_price` | decimal | Minimum price |
| `max_price` | decimal | Maximum price |
| `material` | string | Filter by material (partial match) |
| `color` | string | Filter by color (partial match) |
| `sort` | string | `created_at_desc` (default), `price_asc`, `price_desc`, `name_asc` |
| `page` | int | Page number (default: 1) |
| `limit` | int | Items per page (default: 20) |

### Profile *(requires Bearer token)*

| Method | Path | Description |
|---|---|---|
| `GET` | `/profile` | Get current user's profile |
| `PUT` | `/profile` | Update profile fields (partial update supported) |
| `PUT` | `/profile/password` | Change password (returns 204 No Content) |

### Cart *(requires Bearer token)*

| Method | Path | Description |
|---|---|---|
| `GET` | `/cart` | Get cart with items and totals |
| `POST` | `/cart/items` | Add item to cart (increments quantity if already present) |
| `PUT` | `/cart/items/{product_id}` | Set quantity for a cart item |
| `DELETE` | `/cart/items/{product_id}` | Remove a single item from cart |
| `DELETE` | `/cart` | Clear the entire cart (returns 204) |

### Admin *(requires Bearer token + admin role)*

| Method | Path | Description |
|---|---|---|
| `POST` | `/admin/products` | Create a new product |
| `PUT` | `/admin/products/{id}` | Update a product |
| `DELETE` | `/admin/products/{id}` | Delete a product |
| `POST` | `/admin/categories` | Create a new category |
| `DELETE` | `/admin/categories/{id}` | Delete a category |

---

## Database Schema

### `users`
| Column | Type | Notes |
|---|---|---|
| `id` | integer | Primary key |
| `email` | varchar(255) | Unique, indexed |
| `hashed_password` | varchar(255) | bcrypt hash |
| `first_name` | varchar(100) | Optional |
| `last_name` | varchar(100) | Optional |
| `phone` | varchar(20) | Optional |
| `address` | varchar(500) | Optional |
| `is_admin` | boolean | Default false |
| `created_at` | timestamptz | Server default |

### `categories`
| Column | Type | Notes |
|---|---|---|
| `id` | integer | Primary key |
| `name` | varchar(100) | Display name |
| `slug` | varchar(100) | Unique URL-safe identifier |

### `products`
| Column | Type | Notes |
|---|---|---|
| `id` | integer | Primary key |
| `category_id` | integer | FK to categories, nullable |
| `name` | varchar(255) | Indexed |
| `description` | text | Optional |
| `price` | numeric(10,2) | Exact decimal |
| `material` | varchar(100) | Optional, indexed |
| `color` | varchar(50) | Optional, indexed |
| `stock` | integer | Default 0 |
| `image_url` | varchar(500) | Optional |
| `created_at` | timestamptz | Server default |

### `cart_items`
| Column | Type | Notes |
|---|---|---|
| `id` | integer | Primary key |
| `user_id` | integer | FK to users, indexed |
| `product_id` | integer | FK to products |
| `quantity` | integer | >= 1 |
| `added_at` | timestamptz | Server default |

---

## Project Structure

```
Shop/
├── app/
│   ├── api/
│   │   ├── deps.py               # Shared dependencies (get_db, get_current_user)
│   │   └── v1/
│   │       ├── router.py         # Aggregates all sub-routers
│   │       └── endpoints/
│   │           ├── auth.py
│   │           ├── products.py
│   │           ├── profile.py
│   │           ├── cart.py
│   │           └── admin.py
│   ├── core/
│   │   ├── config.py             # Settings (pydantic-settings)
│   │   └── security.py           # JWT + password hashing
│   ├── crud/                     # Database access functions
│   ├── db/
│   │   ├── base.py               # DeclarativeBase
│   │   └── session.py            # Engine + SessionLocal
│   ├── models/                   # SQLAlchemy ORM models
│   ├── schemas/                  # Pydantic request/response schemas
│   └── main.py                   # FastAPI app entry point
├── alembic/                      # Database migrations
├── frontend/                     # Static HTML/CSS/JS frontend
│   ├── index.html                # Shop catalog
│   ├── product.html              # Product detail
│   ├── cart.html                 # Shopping cart
│   ├── profile.html              # User profile
│   ├── auth.html                 # Login / register
│   ├── admin.html                # Admin panel
│   ├── css/style.css
│   └── js/
│       ├── api.js                # Fetch wrapper + token management
│       ├── auth.js
│       ├── shop.js
│       ├── cart.js
│       ├── profile.js
│       └── admin.js
├── scripts/
│   └── seed_data.py              # Database seeder
├── tests/                        # Test placeholders
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── TESTING_GUIDE.md
└── README.md
```

---

## Development Without Docker

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Set DATABASE_URL in your shell or .env file
# Example: DATABASE_URL=postgresql://shopuser:shoppassword@localhost:5432/shopdb

# Run database migrations
alembic upgrade head

# Seed data (optional)
python -m scripts.seed_data

# Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Stopping the Application

```bash
docker compose down          # Stop containers, preserve data volume
docker compose down -v       # Stop containers and delete all data
```
