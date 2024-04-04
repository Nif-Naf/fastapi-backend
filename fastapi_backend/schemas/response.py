from typing import Any

from fastapi_backend.schemas.abc import BaseSchema


class ResponseSchema(BaseSchema):
    """Схема стандартного ответа."""

    data: Any | None
    message: str
