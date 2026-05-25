"""
Seed the database with categories, products, and demo users.

Usage:
    docker compose exec api python -m scripts.seed_data
    # or locally:
    python -m scripts.seed_data
"""
import sys
import os
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.product import Category, Product
from app.models.cart import CartItem  # noqa: F401 — registers CartItem with SQLAlchemy mapper
from app.models.user import User
from app.core.security import get_password_hash

CATEGORIES = [
    {"name": "Sofas", "slug": "sofas"},
    {"name": "Tables", "slug": "tables"},
    {"name": "Chairs", "slug": "chairs"},
    {"name": "Beds", "slug": "beds"},
    {"name": "Storage", "slug": "storage"},
]

_U = "https://images.unsplash.com/photo-"
_Q = "?w=600&h=400&fit=crop&auto=format"

PRODUCTS = [
    # Sofas
    {
        "category_slug": "sofas",
        "name": "Nordic 3-Seat Sofa",
        "description": "Minimalist Scandinavian-style sofa with solid oak legs and premium fabric upholstery. Perfect for modern living rooms.",
        "price": "1299.99",
        "material": "Fabric",
        "color": "Gray",
        "stock": 12,
        "image_url": f"{_U}1555041469-a586c61ea9bc{_Q}",
    },
    {
        "category_slug": "sofas",
        "name": "Velvet Corner Sofa",
        "description": "Luxurious L-shaped corner sofa in soft velvet. Includes removable cushion covers for easy cleaning.",
        "price": "2199.00",
        "material": "Velvet",
        "color": "Emerald",
        "stock": 5,
        "image_url": f"{_U}1567538096630-e0c55bd6374c{_Q}",
    },
    {
        "category_slug": "sofas",
        "name": "Leather 2-Seat Sofa",
        "description": "Classic two-seater in genuine top-grain leather. Timeless design with deep seat cushions.",
        "price": "1750.00",
        "material": "Leather",
        "color": "Brown",
        "stock": 8,
        "image_url": f"{_U}1540574163026-643ea20ade25{_Q}",
    },
    # Tables
    {
        "category_slug": "tables",
        "name": "Oak Dining Table",
        "description": "Solid oak dining table seats 6 comfortably. Natural grain finish with protective oil coating.",
        "price": "899.00",
        "material": "Oak",
        "color": "Natural",
        "stock": 20,
        "image_url": f"{_U}1533090481720-856c6e3c1fdc{_Q}",
    },
    {
        "category_slug": "tables",
        "name": "Glass Coffee Table",
        "description": "Tempered glass top on a brushed steel frame. Adds a light, airy feel to any living space.",
        "price": "349.99",
        "material": "Glass",
        "color": "Clear",
        "stock": 15,
        "image_url": f"{_U}1493663284031-b7e3aefcae8e{_Q}",
    },
    {
        "category_slug": "tables",
        "name": "Walnut Writing Desk",
        "description": "Compact home office desk in American walnut veneer. Features a cable management cutout.",
        "price": "549.00",
        "material": "Walnut",
        "color": "Dark Brown",
        "stock": 10,
        "image_url": f"{_U}1518455027359-f3f8164ba6bd{_Q}",
    },
    # Chairs
    {
        "category_slug": "chairs",
        "name": "Ergonomic Office Chair",
        "description": "Fully adjustable lumbar support, headrest, and armrests. Breathable mesh back for all-day comfort.",
        "price": "479.00",
        "material": "Mesh",
        "color": "Black",
        "stock": 30,
        "image_url": f"{_U}1589384267710-7a25bc5b4862{_Q}",
    },
    {
        "category_slug": "chairs",
        "name": "Accent Armchair",
        "description": "Statement accent chair in bouclé fabric. Sturdy beech wood frame in a natural finish.",
        "price": "389.00",
        "material": "Bouclé",
        "color": "Cream",
        "stock": 14,
        "image_url": f"{_U}1586023492125-27b2c045efd7{_Q}",
    },
    {
        "category_slug": "chairs",
        "name": "Wooden Dining Chair",
        "description": "Classic bentwood dining chair. Stackable and durable, ideal for dining rooms and kitchens.",
        "price": "129.00",
        "material": "Beech",
        "color": "Natural",
        "stock": 50,
        "image_url": f"{_U}1503602642458-232111445657{_Q}",
    },
    # Beds
    {
        "category_slug": "beds",
        "name": "King Platform Bed",
        "description": "Low-profile platform bed frame in solid pine. No box spring required. Slat support included.",
        "price": "699.00",
        "material": "Pine",
        "color": "White",
        "stock": 9,
        "image_url": f"{_U}1505693314120-0d443867891c{_Q}",
    },
    {
        "category_slug": "beds",
        "name": "Upholstered Bed Frame",
        "description": "Queen-size bed frame with a padded headboard in performance linen. Easy assembly.",
        "price": "849.00",
        "material": "Linen",
        "color": "Beige",
        "stock": 7,
        "image_url": f"{_U}1522771739844-6a9f6d5f14af{_Q}",
    },
    # Storage
    {
        "category_slug": "storage",
        "name": "5-Drawer Dresser",
        "description": "Spacious chest of drawers in oak-effect finish. Smooth-glide metal runners and dovetail joints.",
        "price": "429.00",
        "material": "MDF",
        "color": "Oak",
        "stock": 18,
        "image_url": f"{_U}1556909114-f6e7ad7d3136{_Q}",
    },
    {
        "category_slug": "storage",
        "name": "Modular Bookshelf",
        "description": "Six-cube modular bookshelf. Can be arranged horizontally or vertically. No tools required.",
        "price": "199.00",
        "material": "MDF",
        "color": "White",
        "stock": 25,
        "image_url": f"{_U}1507003211169-0a1dd7228f2d{_Q}",
    },
    {
        "category_slug": "storage",
        "name": "Shoe Cabinet",
        "description": "Slim entryway shoe cabinet with flip-down doors. Holds up to 12 pairs of shoes.",
        "price": "159.00",
        "material": "MDF",
        "color": "Black",
        "stock": 22,
        "image_url": f"{_U}1595526114035-0d45ed16cfbf{_Q}",
    },
    {
        "category_slug": "storage",
        "name": "Wardrobe with Mirror",
        "description": "Three-door wardrobe with a full-length mirror door. Includes hanging rail and two shelves.",
        "price": "789.00",
        "material": "MDF",
        "color": "White",
        "stock": 6,
        "image_url": f"{_U}1558769132-cb1aea458c5e{_Q}",
    },
]


def seed():
    db = SessionLocal()
    try:
        # Seed categories
        cat_map: dict[str, Category] = {}
        for c in CATEGORIES:
            existing = db.query(Category).filter_by(slug=c["slug"]).first()
            if not existing:
                obj = Category(name=c["name"], slug=c["slug"])
                db.add(obj)
                db.flush()
                cat_map[c["slug"]] = obj
            else:
                cat_map[c["slug"]] = existing
        db.commit()
        print(f"  Categories: {len(cat_map)} ready")

        # Seed products
        added = 0
        updated = 0
        for p in PRODUCTS:
            slug = p["category_slug"]
            cat = cat_map[slug]
            existing = db.query(Product).filter_by(name=p["name"]).first()
            if not existing:
                obj = Product(
                    category_id=cat.id,
                    name=p["name"],
                    description=p["description"],
                    price=Decimal(p["price"]),
                    material=p["material"],
                    color=p["color"],
                    stock=p["stock"],
                    image_url=p["image_url"],
                )
                db.add(obj)
                added += 1
            else:
                existing.image_url = p["image_url"]
                updated += 1
        db.commit()
        print(f"  Products: {added} added, {updated} images updated")

        # Seed demo user
        demo = db.query(User).filter_by(email="demo@example.com").first()
        if not demo:
            db.add(User(
                email="demo@example.com",
                hashed_password=get_password_hash("password123"),
                first_name="Demo",
                last_name="User",
                phone="+1 555 0100",
                address="123 Main St, Springfield",
            ))
            print("  Demo user created: demo@example.com / password123")

        # Seed admin user
        admin = db.query(User).filter_by(email="admin@example.com").first()
        if not admin:
            db.add(User(
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                first_name="Admin",
                last_name="User",
                is_admin=True,
            ))
            print("  Admin user created: admin@example.com / admin123")

        db.commit()
        print("Seed complete.")
    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
