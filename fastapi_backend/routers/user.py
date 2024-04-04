import logging
from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from starlette.status import HTTP_200_OK

from fastapi_backend.schemas.response import ResponseSchema
from fastapi_backend.schemas.user import UserSchema
from fastapi_backend.services.authentication import AuthenticationService
from settings import VER_API_ONE

logger = logging.getLogger("development")

user_router = APIRouter(
    prefix=VER_API_ONE + "user",
    tags=["user"],
)


@user_router.get(
    name="None",
    path="/about_me",
    status_code=HTTP_200_OK,
    response_description="None",
    description="""
        None
    """,
)
async def about_me(
    user: Annotated[UserSchema, Depends(AuthenticationService.with_token)],
):
    """Получение всей информации о пользователе."""
    return ResponseSchema(
        data=user,
        message="Here is all the information about you.",
    )
