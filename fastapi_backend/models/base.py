import logging

from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger("development")


class BaseModel(DeclarativeBase):
    """Базовая модель."""

    # def __str__(self):
    #     table: str = self.__tablename__
    #     model_name = " ".join(table.split("_")) if "_" in table else table
    #     return f"Object {model_name.capitalize()}. ID: {self.id}"
