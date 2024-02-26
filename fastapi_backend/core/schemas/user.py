import logging
from datetime import datetime

from pydantic import EmailStr

from ..schemas.abc import BaseSchema

logger = logging.getLogger("dev")


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
