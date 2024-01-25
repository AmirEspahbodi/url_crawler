from pydantic import BaseModel, ConfigDict, EmailStr
from fastapi import Form
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.schema import Security


class UserLoginSchema(BaseModel):
    email: Annotated[EmailStr, Form()]
    password: Annotated[str, Form(min_length=1)]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"email": "amir@amir.com", "password": "Strong_1234"}
        },
        from_attributes=True,
        arbitrary_types_allowed=True,
    )

    async def custom_validations(self, errors, db: AsyncSession, *args, **kwargs):
        Security.ssrf_protection(self.email, "email", errors)
        return errors
