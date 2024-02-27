import logging

from fastapi.routing import APIRouter
from starlette.status import HTTP_201_CREATED

from fastapi_backend.schemas.response import ResponseSchema
from fastapi_backend.schemas.user import UserSchema
from fastapi_backend.services.auth import create_user, uniqueness_check

logger = logging.getLogger("development")

authorization_router = APIRouter(
    prefix="/api/v1/auth",
    tags=[
        "authorization",
    ],
)


@authorization_router.get(path="/this_email_free/{email}/")
def is_unique_email(email) -> ResponseSchema:
    """Проверка на уникальность переданного электронного адреса в БД."""
    response = uniqueness_check(email)
    return response


@authorization_router.post(path="/sign_in", status_code=HTTP_201_CREATED)
def authorization(data: UserSchema) -> ResponseSchema:
    """Создание пользователя и выдача ему прав."""
    response = create_user(data)
    return response
