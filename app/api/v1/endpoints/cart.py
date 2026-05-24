from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.cart import CartItemAdd, CartItemUpdate, CartOut

router = APIRouter()


def _build_cart_response(items) -> CartOut:
    total_price = sum(
        item.product.price * item.quantity for item in items
    )
    return CartOut(
        items=items,
        total_items=sum(i.quantity for i in items),
        total_price=total_price if items else Decimal("0.00"),
    )


@router.get("", response_model=CartOut)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = crud.cart.get_cart(db, current_user.id)
    return _build_cart_response(items)


@router.post("/items", response_model=CartOut, status_code=status.HTTP_201_CREATED)
def add_item(
    data: CartItemAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = crud.product.get_by_id(db, data.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    crud.cart.add_item(db, current_user.id, data)
    items = crud.cart.get_cart(db, current_user.id)
    return _build_cart_response(items)


@router.put("/items/{product_id}", response_model=CartOut)
def update_item(
    product_id: int,
    data: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.quantity < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be at least 1")
    item = crud.cart.update_item(db, current_user.id, product_id, data)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart")
    items = crud.cart.get_cart(db, current_user.id)
    return _build_cart_response(items)


@router.delete("/items/{product_id}", response_model=CartOut)
def remove_item(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    removed = crud.cart.remove_item(db, current_user.id, product_id)
    if not removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart")
    items = crud.cart.get_cart(db, current_user.id)
    return _build_cart_response(items)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    crud.cart.clear_cart(db, current_user.id)
