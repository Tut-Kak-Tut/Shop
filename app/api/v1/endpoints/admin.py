import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_current_admin, get_db
from app.models.user import User
from app.schemas.admin import CategoryCreate, ProductCreate, ProductUpdate
from app.schemas.product import CategoryOut, ProductOut

router = APIRouter()

UPLOAD_DIR = "uploads"
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post("/upload-image")
def upload_image(
    file: UploadFile = File(...),
    _: User = Depends(get_current_admin),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG, WebP, and GIF images are allowed",
        )

    content = file.file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large (maximum 5 MB)",
        )

    ext = file.filename.rsplit(".", 1)[-1].lower() if file.filename and "." in file.filename else "jpg"
    filename = f"{uuid.uuid4().hex}.{ext}"
    dest = os.path.join(UPLOAD_DIR, filename)

    with open(dest, "wb") as f:
        f.write(content)

    return {"url": f"/uploads/{filename}"}


@router.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return crud.product.create_product(db, data)


@router.put("/products/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    product = crud.product.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return crud.product.update_product(db, product, data)


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    product = crud.product.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    crud.product.delete_product(db, product)


@router.post("/categories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return crud.product.create_category(db, data)


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    from app.models.product import Category
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    crud.product.delete_category(db, category)
