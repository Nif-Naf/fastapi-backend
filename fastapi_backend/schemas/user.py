from datetime import datetime

from pydantic import EmailStr

from fastapi_backend.schemas.abc import BaseSchema


class UserSchema(BaseSchema):
    """Схема пользователя."""

    id: int
    first_name: str
    second_name: str
    email: EmailStr
    # password: SecretStr
    password: str
    created_at: datetime
    updated_at: datetime
