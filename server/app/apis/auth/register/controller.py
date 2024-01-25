from uuid import uuid4
from fastapi import status
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security.password import PasswordHandler
from app.core.exception.base import ConnectionException
from app.database import User
from .schema import UserRegisterRequestSchema


class UserRegisterController:
    @staticmethod
    async def create_user(db: AsyncSession, request_body: UserRegisterRequestSchema):
        create_data = request_body.model_dump()
        create_data.update({"password": PasswordHandler.hash(request_body.password)})
        create_data.update({"uuid": str(uuid4())})
        stmt = insert(User).values(**create_data)
        await db.execute(stmt)
        await db.commit()

        # check user created
        stmt = (
            select(User)
            .where(User.email == request_body.email)
            .where(User.is_deleted == False)
        )
        user = (await db.execute(stmt)).scalars().first()
        if user is None:
            raise ConnectionException()

        return user
