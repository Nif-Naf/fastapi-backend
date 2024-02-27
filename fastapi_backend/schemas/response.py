import logging

from fastapi_backend.schemas.base import BaseSchema

logger = logging.getLogger("development")


class ResponseSchema(BaseSchema):
    """Схема стандартного ответа."""

    # Валидация. Один из аргументов обязателен.
    data: dict | None
    message: str | None
