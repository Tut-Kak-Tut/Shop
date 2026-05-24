from fastapi import APIRouter

from app.api.v1.endpoints import admin, auth, cart, products, profile

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(cart.router, prefix="/cart", tags=["cart"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
