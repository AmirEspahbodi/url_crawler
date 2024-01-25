from fastapi import APIRouter, Depends, BackgroundTasks, Security
from typing import Annotated
from app.core.schema.validate import Validate

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.connection.database import connection
from app.core.security.check_auth import AuthenticationRequired
from .schema import (
    PasswordChangeSchema,
)
from .controller import PasswordController as password

password_router = APIRouter()


@password_router.post("/password-change/", summary="user change password")
async def password_change(
    user: Annotated[
        dict[str, int | bool | str],
        Security(AuthenticationRequired.check_auth),
    ],
    db: Annotated[AsyncSession, Depends(connection)],
    request_body: PasswordChangeSchema,
):
    validation_result = await Validate().validate(request_body, db=db)
    return await password.password_change(db, request_body, user)
