import logging

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped

from ..models.abc import BaseModel

logger = logging.getLogger("dev")

__all__ = ("UserModel",)


class UserModel(BaseModel):
    """Модель пользователя."""

    __tablename__ = "fastapi_user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str]
    second_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        comment="Is the user a superuser?",
    )
    is_confirmed: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        comment="Has the user confirmed their email?",
    )
    is_deleted: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        comment="Has this user been deleted?",
    )

    def __str__(self):
        return f"UserModel object. ID: {self.id}"

    def is_super(self) -> bool:
        return self.is_superuser

    def is_confirm(self) -> bool:
        return self.is_confirmed

    def is_delete(self) -> bool:
        return self.is_deleted
