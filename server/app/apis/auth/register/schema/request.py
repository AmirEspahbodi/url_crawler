from datetime import date

from pydantic import BaseModel, ConfigDict, constr, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.schema import Security
from app.database import User


class UserRegisterRequestSchema(BaseModel):
    name: constr(min_length=2) | None
    email: EmailStr
    password: constr(min_length=8)
    birthday: date

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "amir",
                "email": "amir@amir.com",
                "password": "Strong_1234",
                "birthday": "2000-03-09",
            }
        },
        from_attributes=True,
        arbitrary_types_allowed=True,
    )

    async def custom_validations(self, errors, db: AsyncSession, *args, **kwargs):
        Security.ssrf_protection(self.name, "name", errors, nullable=True)
        Security.ssrf_protection(self.email, "email", errors)

        # check admin with this email already exist
        if "email" not in errors:
            stmt = (
                select(User)
                .where(User.email == self.email)
                .where(User.is_deleted == False)
            )
            result = (await db.execute(stmt)).scalars().one_or_none()
            if result is not None:
                if "email" in errors:
                    errors["email"].append("email alerady is in use")
                else:
                    errors["email"] = ["email alerady is in use"]

        return errors
