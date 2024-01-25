from pydantic import BaseModel, ConfigDict, constr
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schema import Security


class UrlRequestSchema(BaseModel):
    url: constr(min_length=2) | None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "url": "https://google.com/",
            }
        },
        from_attributes=True,
        arbitrary_types_allowed=True,
    )

    async def custom_validations(self, errors, db: AsyncSession, *args, **kwargs):
        return errors
