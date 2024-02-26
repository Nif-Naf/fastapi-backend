import logging
from typing import Any

from ..schemas.abc import BaseSchema

logger = logging.getLogger("dev")


class ResponseSchema(BaseSchema):
    """Схема стандартного ответа."""

    data: Any | None
    message: str
