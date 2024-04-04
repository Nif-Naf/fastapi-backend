import logging
from abc import abstractmethod

from fastapi_backend.exceptions.auth import EmailIsNotUnique
from fastapi_backend.exceptions.commnon import DataBaseUnknownError
from fastapi_backend.modules.password import (
    AbstractPasswordModule,
    PasswordModule,
)
from fastapi_backend.repositories.user import (
    AbstractUserRepository,
    UserRepository,
)
from fastapi_backend.schemas.auth import AuthorizationUserSchema
from fastapi_backend.schemas.response import ResponseSchema
from fastapi_backend.services.abc import AbstractService

logger = logging.getLogger("development")


class AbstractAuthorizationService(AbstractService):
    """Сервис для создания нового пользователя."""

    _repository: AbstractUserRepository
    _password_module: AbstractPasswordModule

    def __init__(self, schema: AuthorizationUserSchema):
        self.schema = schema
        self.email = self.schema.email
        self.password = self.schema.password

    @abstractmethod
    async def __call__(self) -> ResponseSchema:
        """Авторизация пользователя.

        Raises:
            EmailIsNotUnique: Если пользователь ввел не уникальный email.
            DataBaseUnknownError: Ошибка при сохранении пользователя.
        """
        raise NotImplementedError


class AuthorizationService(AbstractAuthorizationService):
    _repository = UserRepository
    _password_module = PasswordModule

    def __init__(self, schema: AuthorizationUserSchema):
        super().__init__(schema)

    async def __call__(self) -> ResponseSchema:
        email_is_unique = await self._repository.is_exists(email=self.email)
        if not email_is_unique:
            raise EmailIsNotUnique
        hash_password = self._password_module.get_hash(self.password)
        self.schema.password = hash_password
        data = await self._repository.create(self.schema)
        user, error = data.values()
        if error:
            raise DataBaseUnknownError(error)
        return ResponseSchema(
            data=None,
            message="You are successfully authorized.",
        )
