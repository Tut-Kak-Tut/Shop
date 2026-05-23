import math

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
from app.schemas.product import CategoryOut, ProductFilter, ProductListResponse, ProductOut

router = APIRouter()


@router.get("", response_model=ProductListResponse)
def list_products(filters: ProductFilter = Depends(), db: Session = Depends(get_db)):
    items, total = crud.product.get_products(db, filters)
    pages = math.ceil(total / filters.limit) if filters.limit and total else 0
    return ProductListResponse(
        items=items,
        total=total,
        page=filters.page,
        limit=filters.limit,
        pages=max(pages, 1),
    )


@router.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return crud.product.get_categories(db)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.product.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
