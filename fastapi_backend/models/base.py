from abc import abstractmethod
from datetime import datetime
from typing import Annotated

from pydantic import ValidationError
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.sql.functions import func


# Base model.
class BaseModel(DeclarativeBase):
    """Базовая модель."""

    def convert(self, schema):
        """Конвертировать модель в схему."""
        all_fields = self.__dict__
        all_fields.pop("_sa_instance_state")
        print(all_fields)
        try:
            return schema.model_validate(**all_fields)
        except ValidationError:
            return None


# Data type.
pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(onupdate=func.now)]
