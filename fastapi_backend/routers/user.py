import logging
from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from fastapi_backend.schemas.response import ResponseSchema
from fastapi_backend.schemas.user import UserSchema
from fastapi_backend.services.authentication import AuthenticationService
from fastapi_backend.services.messages import UserMessagesService
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


@user_router.post(
    name="None",
    path="/message/send",
    tags=["message"],
    status_code=HTTP_201_CREATED,
    response_description="None",
    description="""
        None
    """,
)
async def send_message(
    message_body: str,
    user: Annotated[UserSchema, Depends(AuthenticationService.with_token)],
    service: UserMessagesService,
) -> ResponseSchema:
    """Получение всей информации о пользователе."""
    response = service.send_message(user_id=user.id, message_body=message_body)
    return response


@user_router.get(
    name="None",
    path="/message/receive",
    tags=["message"],
    status_code=HTTP_200_OK,
    response_description="None",
    description="""
        None
    """,
)
async def send_message(
    user: Annotated[UserSchema, Depends(AuthenticationService.with_token)],
    service: UserMessagesService,
) -> ResponseSchema:
    """Получение всей информации о пользователе."""
    response = service.receive_message(user_id=user.id)
    return response
