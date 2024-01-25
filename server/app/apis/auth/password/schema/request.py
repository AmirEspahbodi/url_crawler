from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.schema.validate import Password


class PasswordChangeSchema(BaseModel):
    old_password: str
    new_password: str
    new_password_confirm: str
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "old_password": "some old password",
                "new_password": "t445awf23A",
                "new_password_confirm": "t445awf23A",
            }
        }
    )

    async def custom_validations(self, errors, db: AsyncSession, *args, **kwargs):
        Password.contain_lowercase(self.new_password, "new_password", errors)
        Password.contain_uppercase(self.new_password, "new_password", errors)
        Password.contain_numbers(self.new_password, "new_password", errors)
        Password.contain_special_characters(self.new_password, "new_password", errors)
        Password.min_length(self.new_password, 8, "new_password", errors)
        Password.match(
            self.new_password, self.new_password_confirm, "new_password", errors
        )
        return errors
