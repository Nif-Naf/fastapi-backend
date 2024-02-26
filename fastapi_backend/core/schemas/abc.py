import logging

from pydantic import BaseModel

logger = logging.getLogger("dev")


class BaseSchema(BaseModel):
    """Базовая абстрактная схема."""

    ...
