from pydantic import BaseModel, ConfigDict, constr
from datetime import date


class UserSchema(BaseModel):
    name: str | None = None
    email: str
    birthday: date | None = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
