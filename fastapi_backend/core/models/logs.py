import logging

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped

from ..models.abc import BaseModel

logger = logging.getLogger("dev")

__all__ = (
    "UserLogModel",
    "SMTPLogModel",
)


class UserLogModel(BaseModel):
    """Логи пользователя."""

    __tablename__ = "fastapi_user_log"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("fastapi_user.id"),
        nullable=False,
    )
    message: Mapped[int] = mapped_column(nullable=False)
    is_successfully: Mapped[bool] = mapped_column(nullable=False)

    def __str__(self):
        return f"UserLogModel object. ID: {self.id}"


class SMTPLogModel(BaseModel):
    """Логи SMTP сервера."""

    __tablename__ = "fastapi_smtp_log"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(
        ForeignKey("fastapi_user.id"),
        nullable=False,
    )
    type_of_message: Mapped[str] = mapped_column(default="verification_email")
    recipient: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[int] = mapped_column(nullable=False)
