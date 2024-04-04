import logging

from pydantic import BaseModel

logger = logging.getLogger("development")


class BaseSchema(BaseModel):
    """Базовая абстрактная схема."""

    ...
