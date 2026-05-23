import math
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.product import Category, Product
from app.schemas.admin import CategoryCreate, ProductCreate, ProductUpdate
from app.schemas.product import ProductFilter


def get_products(db: Session, filters: ProductFilter) -> tuple[list[Product], int]:
    query = db.query(Product).options(joinedload(Product.category))

    if filters.search:
        term = f"%{filters.search}%"
        query = query.filter(
            or_(Product.name.ilike(term), Product.description.ilike(term))
        )

    if filters.category:
        query = query.join(Product.category).filter(Category.slug == filters.category)

    if filters.min_price is not None:
        query = query.filter(Product.price >= filters.min_price)
    if filters.max_price is not None:
        query = query.filter(Product.price <= filters.max_price)

    if filters.material:
        query = query.filter(Product.material.ilike(f"%{filters.material}%"))
    if filters.color:
        query = query.filter(Product.color.ilike(f"%{filters.color}%"))

    sort_map = {
        "price_asc": Product.price.asc(),
        "price_desc": Product.price.desc(),
        "name_asc": Product.name.asc(),
        "created_at_desc": Product.created_at.desc(),
    }
    order = sort_map.get(filters.sort or "created_at_desc", Product.created_at.desc())
    query = query.order_by(order)

    total = query.count()
    offset = (filters.page - 1) * filters.limit
    items = query.offset(offset).limit(filters.limit).all()

    return items, total


def get_by_id(db: Session, product_id: int) -> Product | None:
    return (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.id == product_id)
        .first()
    )


def get_categories(db: Session) -> list[Category]:
    return db.query(Category).order_by(Category.name).all()


def create_product(db: Session, data: ProductCreate) -> Product:
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return db.query(Product).options(joinedload(Product.category)).filter(Product.id == product.id).first()


def update_product(db: Session, product: Product, data: ProductUpdate) -> Product:
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return db.query(Product).options(joinedload(Product.category)).filter(Product.id == product.id).first()


def delete_product(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()


def create_category(db: Session, data: CategoryCreate) -> Category:
    category = Category(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category: Category) -> None:
    db.delete(category)
    db.commit()
