from fastapi import APIRouter, Depends, status, Request
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schema.validate import Validate
from app.core.connection.database import connection

from .controller import UserRegisterController as register
from .schema import UserRegisterResponseSchema, UserRegisterRequestSchema

register_router = APIRouter()


@register_router.post(
    "/register",
    status_code=status.HTTP_200_OK,
    summary="login admin",
    response_model=UserRegisterResponseSchema,
)
async def login_admin(
    request_body: UserRegisterRequestSchema,
    db: Annotated[AsyncSession, Depends(connection)],
):
    """
    register.
    """

    validation_result = await Validate().validate(request_body, db=db)
    result = await register.create_user(db, request_body)
    return result
