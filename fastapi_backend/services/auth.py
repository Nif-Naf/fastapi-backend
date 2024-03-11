import logging
from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException
from jose import JWTError
from starlette import status

from fastapi_backend.modules.password import PasswordModule
from fastapi_backend.modules.token import TokenModule
from fastapi_backend.schemas.response import ResponseSchema
from fastapi_backend.schemas.user import UserSchema, UserWithPKScheme
from fastapi_backend.services.base import BaseService
from fastapi_backend.utils.exceptions import (
    DecodeTokenFail,
    PasswordsNotMatch,
    TokenExpiration,
    TokenNotTransfer,
    UserNotFound,
)
from settings import OAUTH2_SCHEME

logger = logging.getLogger("development")


class AuthService(BaseService, TokenModule, PasswordModule):
    """Сервис для работы с авторизацией/аутентификацией."""

    def authorization(self, user_schema: UserSchema) -> ResponseSchema:
        """Авторизация пользователя.

        Raises:
            HTTPException: Стандартное HTTP исключение.
        """
        email = user_schema.email
        password = user_schema.password
        email_is_unique = self.orm.is_exists("UserModel", email=email)
        if not email_is_unique:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email address is already taken.",
            )
        user_schema.password = self.get_password_hash(password)
        user_data: dict = user_schema.model_dump()
        _, error = self.orm.create("UserModel", **user_data).values()
        if error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=error,
            )
        return ResponseSchema(
            data=None,
            message="You are successfully authorized.",
        )

    def credentials_authentication(self, email, password) -> UserWithPKScheme:
        """Аутентификация пользователя по связке логин-пароль.

        Args:
            email (str): Электронный адрес.
            password (str): Пароль.

        Raises:
            UserNotFound: Пользователь не найден
            TokenExpiration: Пароль не подходит.
        """
        user, error = self.orm.get_one("UserModel", email=email).values()
        if user is None or error:
            raise UserNotFound
        check_password = self.verify_password(password, user.password)
        if not check_password:
            raise PasswordsNotMatch
        return user

    def token_authentication(
        self,
        token: Annotated[str, Depends(OAUTH2_SCHEME)],
    ) -> UserWithPKScheme:
        """Аутентификация пользователя по токену.

        Raises:
            TokenNotTransfer: Токен не передан.
            DecodeTokenFail: Не валидный токен.
            TokenExpiration: Токен пророчен.
            UserNotFound: Пользователь не найден.
        """
        if not token:
            raise TokenNotTransfer
        try:
            token_data = self.decode_token(token)
        except JWTError:
            raise DecodeTokenFail
        email: str = token_data["sub"]
        expiration: datetime = token_data["exp"]
        if expiration < datetime.now():
            raise TokenExpiration
        user, error = self.orm.get_one(email=email).values()
        if user is None or error:
            raise UserNotFound
        return user
