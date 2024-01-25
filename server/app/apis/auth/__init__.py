from fastapi import APIRouter

from .login.router import login_router
from .password.router import password_router
from .register.router import register_router

auth_router = APIRouter(prefix="/auth")

auth_router.include_router(login_router, tags=["Auth"])
auth_router.include_router(password_router, tags=["Auth"])
auth_router.include_router(register_router, tags=["Auth"])

__all__ = ["auth_router"]
