import logging

from fastapi_backend.schemas.base import BaseSchema
from fastapi_backend.schemas.token import Token

logger = logging.getLogger("development")


class BaseResponseSchema(BaseSchema):
    message: str | None


class ResponseSchema(BaseResponseSchema):
    """Схема стандартного ответа."""

    data: dict | None


class TokenResponseSchema(BaseResponseSchema):
    """Схема стандартного ответа."""

    data: Token | None
