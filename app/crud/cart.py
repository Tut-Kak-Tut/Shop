from sqlalchemy.orm import Session, joinedload

from app.models.cart import CartItem
from app.models.product import Product
from app.schemas.cart import CartItemAdd, CartItemUpdate


def get_cart(db: Session, user_id: int) -> list[CartItem]:
    return (
        db.query(CartItem)
        .options(joinedload(CartItem.product).joinedload(Product.category))
        .filter(CartItem.user_id == user_id)
        .all()
    )


def add_item(db: Session, user_id: int, data: CartItemAdd) -> CartItem:
    existing = (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id, CartItem.product_id == data.product_id)
        .first()
    )
    if existing:
        existing.quantity += data.quantity
        db.commit()
        db.refresh(existing)
        return existing

    item = CartItem(user_id=user_id, product_id=data.product_id, quantity=data.quantity)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(db: Session, user_id: int, product_id: int, data: CartItemUpdate) -> CartItem | None:
    item = (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id, CartItem.product_id == product_id)
        .first()
    )
    if not item:
        return None
    item.quantity = data.quantity
    db.commit()
    db.refresh(item)
    return item


def remove_item(db: Session, user_id: int, product_id: int) -> bool:
    item = (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id, CartItem.product_id == product_id)
        .first()
    )
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def clear_cart(db: Session, user_id: int) -> int:
    deleted = (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id)
        .delete(synchronize_session=False)
    )
    db.commit()
    return deleted
