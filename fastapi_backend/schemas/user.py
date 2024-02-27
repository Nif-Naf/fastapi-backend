import logging

from fastapi_backend.schemas.base import BaseSchema

logger = logging.getLogger("development")


class UserSchema(BaseSchema):
    """Схема пользователя без первичного ключа.
    Запись которой нет в БД.
    """

    name: str
    username: str
    email: str
    password: str


class UserWithPKScheme(UserSchema):
    """Схема пользователя с первичным ключом.
    Запись которой уже в БД.
    """

    id: str
