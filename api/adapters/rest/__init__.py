from fastapi import APIRouter
from api.adapters.rest import users, products

api_router = APIRouter()

api_router.include_router(users.router, prefix="/zebrands-system/users")
api_router.include_router(products.router, prefix="/zebrands-system/product")
