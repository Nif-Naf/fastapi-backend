from datetime import datetime
from typing import Annotated

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.sql.functions import func

# Data type.
pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[
    datetime,
    mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    ),
]
str_50 = Annotated[str, 50]


class BaseModel(DeclarativeBase):
    """Базовая модель."""

    type_annotation_map = {
        str_50: String(50),
    }
