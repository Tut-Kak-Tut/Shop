from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class ProductCreate(BaseModel):
    category_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: Decimal
    material: Optional[str] = None
    color: Optional[str] = None
    stock: int = 0
    image_url: Optional[str] = None


class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    material: Optional[str] = None
    color: Optional[str] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None


class CategoryCreate(BaseModel):
    name: str
    slug: str
