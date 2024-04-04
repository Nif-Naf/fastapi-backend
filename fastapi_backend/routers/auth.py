import logging
from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from fastapi_backend.form.auth import OAuth2CredentialsRequestForm
from fastapi_backend.schemas.auth import AuthorizationUserSchema, TokenSchema
from fastapi_backend.schemas.response import ResponseSchema
from fastapi_backend.services.authentication import AuthenticationService
from fastapi_backend.services.authorization import AuthorizationService
from settings import VER_API_ONE

logger = logging.getLogger("development")

##############################################################################
# Router.
##############################################################################
auth_router = APIRouter(
    prefix=VER_API_ONE + "auth",
)

##############################################################################
# Responses for docs.
##############################################################################
sign_up_responses = {
    HTTP_409_CONFLICT: {
        "description": "The transmitted email address is not unique within "
        "the database.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "This email is already in use by another "
                    "user.",
                },
            },
        },
    },
    HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Any database error when saving the user.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Any error related to saving the user to "
                    "the database.",
                },
            },
        },
    },
}

login_responses = {
    HTTP_403_FORBIDDEN: {
        "description": "The password for the found user does not match.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Passwords did not match.",
                },
            },
        },
    },
    HTTP_404_NOT_FOUND: {
        "description": "The user was not found based on the login provided.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "A user with this login was not found.",
                },
            },
        },
    },
    HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Any database error when searching the user.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "string",
                },
            },
        },
    },
}


##############################################################################
# API.
##############################################################################
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
