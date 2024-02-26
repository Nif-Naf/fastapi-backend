import logging
from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from backend.forms.auth import OAuth2CredentialsRequestForm
from backend.responses.auth_response import login_responses, sign_up_responses
from backend.settings import VER_API_ONE
from core.schemas.auth import AuthorizationUserSchema, TokenSchema
from core.schemas.response import ResponseSchema

from ..services.authentication import AuthenticationService
from ..services.authorization import AuthorizationService

__all__ = ("auth_router",)

logger = logging.getLogger("dev")


auth_router = APIRouter(
    prefix=VER_API_ONE + "auth",
)


@auth_router.post(
    name="Authorization new user.",
    path="/sign_up",
    tags=["authorization"],
    status_code=HTTP_201_CREATED,
    response_description="You are successfully authorized.",
    responses=sign_up_responses,
    description="Create a new user and add it to the database.",
)
async def sign_up(
    user_fields: AuthorizationUserSchema,
) -> ResponseSchema:
    """Регистрация."""
    init_service = AuthorizationService(schema=user_fields)
    response = await init_service()
    return response


@auth_router.post(
    name="Authenticate an existing user.",
    path="/login",
    tags=["authentication"],
    status_code=HTTP_200_OK,
    response_description="You are successfully authenticated.",
    responses=login_responses,
    description="""
        Search for a user in the database by login. And creating an
        access token for it.
    """,
)
async def login(
    form_data: Annotated[OAuth2CredentialsRequestForm, Depends()],
) -> TokenSchema:
    """Вход в систему."""
    credentials = form_data.credentials
    _, token = await AuthenticationService.with_credentials(credentials)
    return TokenSchema(access_token=token)
