import logging

from sqlalchemy.orm import Mapped, mapped_column

from fastapi_backend.models.base import BaseModel

logger = logging.getLogger("development")


class UserModel(BaseModel):
    """Модель пользователя."""

    __tablename__ = "user"
    name: Mapped[str]
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
