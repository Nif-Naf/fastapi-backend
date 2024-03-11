from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.sql.functions import func


# Base model.
class BaseModel(DeclarativeBase):
    """Базовая модель."""

    ...


# Data type.
pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(onupdate=func.now)]
