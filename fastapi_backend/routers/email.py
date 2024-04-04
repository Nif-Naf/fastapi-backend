import logging
from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from starlette.status import HTTP_200_OK

from fastapi_backend.schemas.response import ResponseSchema
from fastapi_backend.services.email import AbstractEmailService, EmailService
from fastapi_backend.typing.base import Email
from settings import VER_API_ONE

logger = logging.getLogger("development")

email_router = APIRouter(
    prefix=VER_API_ONE + "email",
    tags=["email"],
)


@email_router.get(
    name="Checking the uniqueness of the email address within the database.",
    path="/is_this_free/{email}",
    tags=["authorization"],
    status_code=HTTP_200_OK,
    response_description="The transmitted email is unique in the database.",
    description="""
        Since the email field in the database is unique. Then each user"
        must have a unique email address.
    """,
)
async def is_unique_email(
    email: Email,
    service: Annotated[AbstractEmailService, Depends(EmailService)],
) -> ResponseSchema:
    """Проверка на уникальность переданного электронного адреса в БД."""
    response = await service.this_email_is_unique(email)
    return response
