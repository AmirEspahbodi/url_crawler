from fastapi import APIRouter, Depends, status, Request
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.schema.validate import Validate
from app.core.connection.database import connection

from .schema import (
    UserLoginSchema,
)
from .controller import AdminController as admin

login_router = APIRouter()


@login_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="login admin",
)
async def login_admin(
    request_body: UserLoginSchema,
    db: Annotated[AsyncSession, Depends(connection)],
):
    """
    login admin.

    Request Body:
    - `email`: **string**, admin email
    - `password`: **string**, admin password


    Returns:
    - JSON response containing the jwt token and admin information if email and password are correct.

    Summary:
    admin login.
    """

    validation_result = await Validate().validate(request_body, db=db)
    result = await admin.admin_login(db, request_body)
    return result
