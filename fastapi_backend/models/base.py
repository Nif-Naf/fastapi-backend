import logging

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

logger = logging.getLogger("development")


class BaseModel(DeclarativeBase):
    """Базовая модель."""

    id: Mapped[int] = mapped_column(primary_key=True)

    def __str__(self):
        table: str = self.__tablename__
        model_name = " ".join(table.split("_")) if "_" in table else table
        return f"Object {model_name.capitalize()}. ID: {self.id}"
