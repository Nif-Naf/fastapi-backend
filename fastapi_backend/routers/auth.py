import logging
from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_201_CREATED

from fastapi_backend.schemas.response import ResponseSchema
from fastapi_backend.schemas.token import Token
from fastapi_backend.schemas.user import UserSchema
from fastapi_backend.services.auth import (
    authenticate_user,
    authorization_user,
    check_email_user,
    create_token_for_user,
)
from settings import AUTH_PREFIX

logger = logging.getLogger("development")

auth_router = APIRouter(
    prefix=AUTH_PREFIX,
)


@auth_router.get(
    path="/this_email_free/{email}",
    tags=[
        "authorization",
    ],
)
def is_unique_email(email) -> ResponseSchema:
    """Проверка на уникальность переданного электронного адреса в БД."""
    response = check_email_user(email)
    return response


@auth_router.post(
    path="/sign_in",
    tags=[
        "authorization",
    ],
    status_code=HTTP_201_CREATED,
)
def sign_in(data: UserSchema) -> ResponseSchema:
    """Создание пользователя и выдача ему прав."""
    response = authorization_user(data)
    return response


@auth_router.post(
    path="/login",
    tags=[
        "authentication",
    ],
    status_code=HTTP_201_CREATED,
)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Аутентификация пользователя по паролю и почте."""
    user = authenticate_user(form_data.username, form_data.password)
    response = create_token_for_user(user.email)
    return response
