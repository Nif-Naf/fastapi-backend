import logging

from fastapi_backend.schemas.base import BaseSchema

logger = logging.getLogger("development")


class ResponseSchema(BaseSchema):
    """Схема стандартного ответа."""

    data: dict | None
    message: str | None
