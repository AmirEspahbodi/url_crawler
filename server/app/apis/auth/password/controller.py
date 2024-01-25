from uuid import uuid4
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security.password import PasswordHandler
from app.core.exception.base import (
    ConnectionException,
    UnprocessableEntity,
)
from app.core.utils.logger.logger import logger
from app.database import User
from .schema import PasswordChangeSchema


class PasswordController:
    @staticmethod
    async def password_change(
        db: AsyncSession, request_body: PasswordChangeSchema, user
    ):
        if not PasswordHandler.verify(request_body.old_password, user.password):
            raise UnprocessableEntity(message="incorrect password")
        stmt = (
            update(User)
            .filter(User.id == user.get("admin_id"))
            .filter(User.is_deleted == False)
            .values(
                password=PasswordHandler.hash(request_body.new_password),
                uuid=str(uuid4()),
            )
        )
        try:
            await db.execute(stmt)
            await db.commit()
        except BaseException as e:
            logger.error("password_change ---> Alchemy Exception ---> " + str(e))
            raise ConnectionException()

        return {"message": "password changed successfully"}
