import logging
from datetime import datetime

from sqlalchemy.orm.base import Mapped
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.sql.functions import func

logger = logging.getLogger("dev")



class BaseModel(DeclarativeBase):
    """Базовая модель."""

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )
