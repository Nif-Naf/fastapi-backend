import logging

from sqlalchemy.orm import Mapped, mapped_column

from fastapi_backend.models.base import BaseModel

logger = logging.getLogger("development")


class UserModel(BaseModel):
    """Модель пользователя."""

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    def __str__(self):
        return f"UserModel object. ID: {self.id}"
