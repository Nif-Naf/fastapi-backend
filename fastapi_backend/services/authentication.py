import logging
from abc import abstractmethod
from typing import Annotated

from fastapi import Depends
from jose import ExpiredSignatureError, JWTError

from fastapi_backend.exceptions import auth as exceptions
from fastapi_backend.exceptions.commnon import DataBaseUnknownError
from fastapi_backend.modules.password import (
    AbstractPasswordModule,
    PasswordModule,
)
from fastapi_backend.modules.token import AbstractTokenModule, TokenModule
from fastapi_backend.repositories.user import (
    AbstractUserRepository,
    UserRepository,
)
from fastapi_backend.schemas.auth import CredentialsSchema
from fastapi_backend.schemas.user import UserSchema
from fastapi_backend.services.abc import AbstractService
from fastapi_backend.typing.base import JWTToken
from settings import OAUTH2_SCHEME

logger = logging.getLogger("development")


class AbstractAuthenticationService(AbstractService):
    """Сервис для аутентификации пользователя."""

    _repository: AbstractUserRepository
    _password_module: AbstractPasswordModule
    _token_module: AbstractTokenModule

    @classmethod
    @abstractmethod
    async def with_credentials(
        cls,
        credentials: CredentialsSchema,
        create_token: bool = True,
    ) -> tuple[UserSchema, JWTToken | None]:
        """Аутентификация пользователя по связке логин-пароль.

        Raises:
            PasswordsNotMatch: Пароль не подошел.
            UserNotFound: Пользователь не найден.
            CommonUnknownError: Если при поиске пользователя возникла ошибка.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def with_token(
        cls,
        token: Annotated[JWTToken, Depends(OAUTH2_SCHEME)],
    ) -> UserSchema:
        """Аутентификация пользователя по токену.

        Raises:
            TokenNotTransfer: Токен не передан.
            DecodeTokenFail: Не валидный токен.
            TokenExpiration: Токен просрочен.
            UserNotFound: Пользователь не найден.
            CommonUnknownError: Если при поиске пользователя возникла ошибка.
        """
        raise NotImplementedError


class AuthenticationService(AbstractAuthenticationService):
    _repository = UserRepository
    _password_module = PasswordModule
    _token_module = TokenModule

    @classmethod
    async def with_credentials(
        cls,
        credentials: CredentialsSchema,
        create_token=True,
    ) -> tuple[UserSchema, JWTToken | None]:
        token = None
        email, password = credentials.username, credentials.password
        data = await cls._repository.find_one(email=email)
        user, error = data.values()
        if user is None:
            raise exceptions.UserNotFound
        elif error:
            raise DataBaseUnknownError(error)
        user_password = user.password
        check_password = cls._password_module.verify_password(
            password=password,
            hashed_password=user_password,
        )
        if not check_password:
            raise exceptions.PasswordsNotMatch
        if create_token:
            token = cls._token_module.create_token(email=user.email)
        return user, token

    @classmethod
    async def with_token(
        cls,
        token: Annotated[JWTToken, Depends(OAUTH2_SCHEME)],
    ) -> UserSchema:
        if not token:
            raise exceptions.TokenNotTransfer
        try:
            token_data = cls._token_module.decode_token(token)
        except ExpiredSignatureError:
            raise exceptions.TokenExpiration
        except JWTError:
            raise exceptions.DecodeTokenFail
        email: str = token_data["sub"]
        data = await cls._repository.find_one(email=email)
        user, error = data.values()
        if user is None:
            raise exceptions.UserNotFound
        elif error:
            raise DataBaseUnknownError(error)
        return user
