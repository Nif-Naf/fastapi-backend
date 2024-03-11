import logging

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped

from fastapi_backend.models import base as data_type
from fastapi_backend.models.base import BaseModel

logger = logging.getLogger("development")


class UserModel(BaseModel):
    """Модель пользователя."""

    __tablename__ = "users"
    id: Mapped[data_type.pk]
    name: Mapped[str]
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    # created_at: Mapped[data_type.created_at]
    # updated_at: Mapped[data_type.updated_at]

    def __str__(self):
        return f"UserModel object. ID: {self.id}"
