from datetime import date
from pydantic import BaseModel, ConfigDict


class UrlResponseSchema(BaseModel):
    id: int
    title: str | None = None
    icon: str | None = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
