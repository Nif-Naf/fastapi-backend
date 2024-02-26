import logging
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.functions import func

logger = logging.getLogger("dev")

__all__ = ("BaseModel",)

Base = declarative_base()


class BaseModel(Base):
    """Базовая модель."""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )
