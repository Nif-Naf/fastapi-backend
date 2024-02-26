import logging
from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from starlette.status import HTTP_200_OK

from fastapi_backend.core.schemas.response import ResponseSchema
from fastapi_backend.core.schemas.user import UserSchema
from fastapi_backend.core.settings import VER_API_ONE

from ..services.authentication import AuthenticationService

logger = logging.getLogger("dev")

user_router = APIRouter(
    prefix=VER_API_ONE + "user",
    tags=["user"],
)


@user_router.get(
    name="None",
    path="/info",
    status_code=HTTP_200_OK,
    response_description="None",
    description="""
        None
    """,
)
async def about_me(
    user: Annotated[UserSchema, Depends(AuthenticationService.with_token)],
):
    """ """
    ...

@user_router.patch(
    name="None",
    path="/update",
    status_code=HTTP_200_OK,
    response_description="None",
    description="""
        None
    """,
)
async def update_me(
    user: Annotated[UserSchema, Depends(AuthenticationService.with_token)],
):
    """ """
    ...

@user_router.delete(
    name="None",
    path="/delete",
    status_code=HTTP_200_OK,
    response_description="None",
    description="""
        None
    """,
)
async def delete_me(
    user: Annotated[UserSchema, Depends(AuthenticationService.with_token)],
):
    """ """
    ...

@user_router.get(
    name="None",
    path="/forget_password",
    status_code=HTTP_200_OK,
    response_description="None",
    description="""
        None
    """,
)
async def delete_me(
    user: Annotated[UserSchema, Depends(AuthenticationService.with_token)],
):
    """ """
    ...

@user_router.patch(
    name="None",
    path="/change_password",
    status_code=HTTP_200_OK,
    response_description="None",
    description="""
        None
    """,
)
async def delete_me(
        user: Annotated[UserSchema, Depends(AuthenticationService.with_token)],
):
    """ """
    ...