from fastapi import APIRouter

from .auth import auth_router
from .urls import url_router

root_api_router = APIRouter()

root_api_router.include_router(auth_router)
root_api_router.include_router(url_router)

__all__ = ["root_api_router"]
