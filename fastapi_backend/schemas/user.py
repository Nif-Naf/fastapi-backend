import logging

from fastapi_backend.schemas.base import BaseSchema

logger = logging.getLogger("development")


class UserSchema(BaseSchema):
    """Схема пользователя."""

    id: int
    name: str
    username: str
    email: str
    password: str
