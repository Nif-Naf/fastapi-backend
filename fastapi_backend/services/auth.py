import logging

from fastapi import HTTPException
from starlette import status

from fastapi_backend.repositories.password import PasswordRepository
from fastapi_backend.repositories.user import UserRepository
from fastapi_backend.schemas.response import ResponseSchema
from fastapi_backend.schemas.user import UserSchema

logger = logging.getLogger("development")


def create_user(data: UserSchema) -> ResponseSchema:
    """Логика авторизации.
    - Валидация полей.
    - Проверка уникальности почты в базе.
    - Хеширование пароля.
    - Создание записи в таблице.

    Raises:
        HTTPException - При любых ошибках.
    """
    email = data.email
    password = data.password
    email_is_unique = UserRepository.email_user_is_unique(email)
    if not email_is_unique:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email address is already taken.",
        )
    data.password = PasswordRepository.get_password_hash(password)
    create = UserRepository.create_user_repository(data)
    if error := create["error"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error,
        )
    return ResponseSchema(
        data=None,
        message="You are successfully authorized.",
    )


def uniqueness_check(email: str) -> ResponseSchema:
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
