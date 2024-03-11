import logging

from fastapi.routing import APIRouter

from fastapi_backend.schemas.response import ResponseSchema
from fastapi_backend.services.email import EmailService

logger = logging.getLogger("development")

email_router = APIRouter(
    prefix="/api/v1/email",
    tags=[
        "email",
    ],
)


@email_router.get(path="/is_this_free/{email}")
def is_unique_email(email) -> ResponseSchema:
    """Проверка на уникальность переданного электронного адреса в БД."""
    service = EmailService()
    response = service.check_email_user(email)
    return response
