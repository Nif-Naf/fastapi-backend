import logging
from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from starlette.status import HTTP_200_OK

from backend.services.authentication import AuthenticationService
from backend.services.email import AbstractEmailService, EmailService
from backend.settings import VER_API_ONE
from core.schemas.response import ResponseSchema
from core.schemas.user import UserSchema

__all__ = ("email_router",)

logger = logging.getLogger("dev")

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
    email: str,
    service: Annotated[AbstractEmailService, Depends(EmailService)],
) -> ResponseSchema:
    """Проверка на уникальность переданного электронного адреса в БД."""
    response = await service.this_email_is_unique(email)
    return response


@email_router.post(
    name="Send short code in latter for confirmation user email.",
    path="/send/confirmation_code",
    status_code=HTTP_200_OK,
    response_description="The code in latter is send.",
    description="""
        It is necessary to check each email address entered by the user 
        to work with the platform. Here we send a confirmation email.
    """,
)
async def send_confirmation_code(
    user: Annotated[UserSchema, Depends(AuthenticationService.with_token)],
) -> ResponseSchema:
    """ """
    ...


@email_router.get(
    name="Confirm your email address using the short code sent to you.",
    path="/approve/confirmation_code/{code}",
    status_code=HTTP_200_OK,
    response_description="Email is confirm.",
    description="""
        It is necessary to check each email address entered by the user 
        to work with the platform. Here we a confirmate email.
    """,
)
async def enter_confirmation_code(
    user: Annotated[UserSchema, Depends(AuthenticationService.with_token)],
) -> ResponseSchema:
    """ """
    ...
