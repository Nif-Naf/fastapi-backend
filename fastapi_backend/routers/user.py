import logging
from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter

from fastapi_backend.schemas.user import UserWithPKScheme as User
from fastapi_backend.services.auth import AuthService
from settings import VER_API_ONE

logger = logging.getLogger("development")

user_router = APIRouter(
    prefix=VER_API_ONE + "user",
    tags=[
        "user",
    ],
)


@user_router.get(path="/about_me")
def about_me(
    current_user: Annotated[User, Depends(AuthService.token_authentication)],
):
    """Получение всей информации о пользователе.
    Без хэша пароля.
    """
    current_user.password = None
    return current_user
