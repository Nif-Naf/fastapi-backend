import logging

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped

from fastapi_backend.models import abc as data_type
from fastapi_backend.models.abc import BaseModel, str_50

logger = logging.getLogger("development")


class UserModel(BaseModel):
    """Модель пользователя."""

    __tablename__ = "fastapi_user"
    id: Mapped[data_type.pk]
    first_name: Mapped[str_50]
    second_name: Mapped[str_50]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[data_type.created_at]
    updated_at: Mapped[data_type.updated_at]

    def __str__(self):
        return f"UserModel object. ID: {self.id}"
