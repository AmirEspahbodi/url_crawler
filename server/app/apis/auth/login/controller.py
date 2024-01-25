from uuid import uuid4
from fastapi import Request
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security.password import PasswordHandler
from app.core.exception.base import NotFoundException
from app.core.security.jwt import JWTHandler
from app.database import User
from .schema import UserLoginSchema


class AdminController:
    @staticmethod
    async def admin_login(db: AsyncSession, request_body: UserLoginSchema):
        stmt = (
            select(User)
            .where(User.email == request_body.email)
            .where(User.is_deleted == False)
            # .where(Admin.status == 1)
        )
        user = (await db.execute(stmt)).scalars().first()

        if user is None or not PasswordHandler.verify(
            request_body.password, user.password
        ):
            raise NotFoundException(
                message="email or password is wrong",
                error={"access": ["email or password is wrong"]},
            )

        jwt = JWTHandler.encode(
            {
                "user_id": user.id,
                "uuid": user.uuid,
                "is_admin": user.is_admin,
            }
        )
        return {
            "user_id": user.id,
            "name": user.name,
            "token": jwt,
        }
