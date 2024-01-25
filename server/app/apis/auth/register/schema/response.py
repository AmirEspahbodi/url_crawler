from datetime import date
from pydantic import BaseModel, ConfigDict


class UserRegisterResponseSchema(BaseModel):
    name: str | None = None
    email: str
    birthday: date | None = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
