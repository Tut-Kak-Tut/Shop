from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    price: Decimal
    material: Optional[str]
    color: Optional[str]
    stock: int
    image_url: Optional[str]
    category: Optional[CategoryOut]


class ProductFilter(BaseModel):
    search: Optional[str] = None
    category: Optional[str] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    material: Optional[str] = None
    color: Optional[str] = None
    sort: Optional[str] = "created_at_desc"
    page: int = 1
    limit: int = 20


class ProductListResponse(BaseModel):
    items: list[ProductOut]
    total: int
    page: int
    limit: int
    pages: int
