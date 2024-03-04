import logging
from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter

from fastapi_backend.repositories.user import UserRepository
from fastapi_backend.schemas.user import UserWithPKScheme as User

logger = logging.getLogger("development")

email_router = APIRouter(
    prefix="/api/v1/email",
    tags=[
        "email",
    ],
)


@email_router.get(path="/send_code")
def send_verification_code(
    current_user: Annotated[User, Depends(UserRepository.get_current_user)],
):
    """Отправка электронного письма на электронный ящик пользователя со
    специальным кодом. Для подтверждения почты пользователя.

    Код храниться n количество времени в кэше. Далее затирается.
    """
    # user = ...
    # response_content = ...
    # return JSONResponse(content=response_content)
    return current_user


@email_router.post(path="/verification")
def verification_email(
    current_user: Annotated[User, Depends(UserRepository.get_current_user)],
):
    """Подтверждение почты с помощью специального кода.
    Проверка введенного специального кода с тем что был отправлен.
    """
    # user = ...
    # response_content = ...
    # return JSONResponse(content=response_content)
    return current_user
