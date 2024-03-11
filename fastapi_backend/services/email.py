import logging

from fastapi_backend.schemas.response import ResponseSchema
from fastapi_backend.services.base import BaseService

logger = logging.getLogger("development")


class EmailService(BaseService):
    """Сервис для работы с электронной почтой."""

    def check_email_user(self, email: str) -> ResponseSchema:
        """Проверка на уникальность email в рамках БД."""
        is_unique = self.orm.is_exists("UserModel", email=email)
        data = {"unique": is_unique}
        if is_unique:
            return ResponseSchema(
                data=data,
                message="This address is unique in the database.",
            )
        return ResponseSchema(
            data=data,
            message="This address is not unique in the database.",
        )
