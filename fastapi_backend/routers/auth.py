import logging
from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_201_CREATED

from fastapi_backend.schemas.response import ResponseSchema
from fastapi_backend.schemas.token import Token
from fastapi_backend.schemas.user import UserSchema
from fastapi_backend.services.auth import AuthService
from settings import VER_API_ONE

logger = logging.getLogger("development")

auth_router = APIRouter(
    prefix=VER_API_ONE + "auth",
)


@auth_router.post(
    path="/sign_in",
    tags=[
        "authorization",
    ],
    status_code=HTTP_201_CREATED,
)
def sign_up(data: UserSchema) -> ResponseSchema:
    """Регистрация."""
    service = AuthService()
    response = service.authorization(data)
    return response


@auth_router.post(
    path="/login",
    tags=[
        "authentication",
    ],
)
def sign_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Вход в систему."""
    service = AuthService()
    email: str = form_data.username
    password: str = form_data.password
    user = service.credentials_authentication(email, password)
    response = service.create_token(user.email)
    return response
