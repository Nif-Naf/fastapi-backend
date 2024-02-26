import logging
from abc import abstractmethod

from backend.modules.password import AbstractPasswordModule, PasswordModule
from backend.repositories.user import AbstractUserRepository, UserRepository
from backend.services.abc import AbstractService
from core.schemas.auth import AuthorizationUserSchema
from core.schemas.response import ResponseSchema
from core.startlet_exceptions.auth import EmailIsNotUnique
from core.startlet_exceptions.commnon import DataBaseUnknownError

logger = logging.getLogger("dev")


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
