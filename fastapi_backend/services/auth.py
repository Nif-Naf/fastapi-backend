import logging

from fastapi import HTTPException
from starlette import status

from fastapi_backend.repositories.password import PasswordRepository
from fastapi_backend.repositories.token import TokenRepository
from fastapi_backend.repositories.user import UserRepository
from fastapi_backend.schemas.response import ResponseSchema
from fastapi_backend.schemas.token import Token
from fastapi_backend.schemas.user import UserSchema, UserWithPKScheme

logger = logging.getLogger("development")


def authorization_user(data: UserSchema) -> ResponseSchema:
    """Авторизация пользователя."""
    email = data.email
    password = data.password
    email_is_unique = UserRepository.email_user_is_unique(email)
    if not email_is_unique:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email address is already taken.",
        )
    data.password = PasswordRepository.get_password_hash(password)
    create = UserRepository.create_user(data)
    if error := create["error"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error,
        )
    return ResponseSchema(
        data=None,
        message="You are successfully authorized.",
    )


def authenticate_user(email: str, password: str) -> UserWithPKScheme:
    """Аутентификация пользователя."""
    err_atr = {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "headers": {"WWW-Authenticate": "Bearer"},
    }
    user, error = UserRepository.find_user(email=email).values()
    if error:
        raise HTTPException(detail=error, **err_atr)
    check_password = PasswordRepository.verify_password(
        password,
        user.password,
    )
    if not check_password:
        raise HTTPException(detail="Incorrect password", **err_atr)
    return user


def create_token_for_user(email: str) -> Token:
    """Создание токена доступа в систему для пользователя."""
    token = TokenRepository.create(email)
    return token
    # return TokenResponseSchema(
    #     data=token,
    #     message="You have been successfully authenticated.",
    # )


def check_email_user(email: str) -> ResponseSchema:
    """Проверка на уникальность email в рамках БД."""
    is_unique = UserRepository.email_user_is_unique(email)
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
