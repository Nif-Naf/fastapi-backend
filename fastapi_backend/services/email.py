import logging
from abc import abstractmethod

from fastapi_backend.repositories.user import UserRepository
from fastapi_backend.schemas.response import ResponseSchema
from fastapi_backend.services.abc import AbstractService
from fastapi_backend.typing.base import Email

logger = logging.getLogger("development")


class AbstractEmailService(AbstractService):
    """Сервис для работы с электронной почтой."""

    _repository = UserRepository

    @classmethod
    @abstractmethod
    async def this_email_is_unique(
        cls,
        email: Email,
    ) -> ResponseSchema:
        """Проверка на уникальность email в рамках БД."""
        raise NotImplementedError


class EmailService(AbstractEmailService):
    @classmethod
    async def this_email_is_unique(
        cls,
        email: Email,
    ) -> ResponseSchema:
        is_uniq = await cls._repository.is_exists(email=email)
        data = {"unique": is_uniq}
        return ResponseSchema(
            data=data,
            message=f"This address {'is' if is_uniq else 'is not'} unique.",
        )
