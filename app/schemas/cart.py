from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.schemas.product import ProductOut


class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product: ProductOut
    quantity: int


class CartOut(BaseModel):
    items: list[CartItemOut]
    total_items: int
    total_price: Decimal
