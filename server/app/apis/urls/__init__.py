from fastapi import APIRouter

from .router import url_router as sub_url_router

url_router = APIRouter(prefix="/url")
url_router.include_router(sub_url_router, tags=["Url"])

__all__ = ["url_router"]
