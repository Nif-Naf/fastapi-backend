import logging
from typing import Annotated

from pydantic import AfterValidator, EmailStr

from fastapi_backend.schemas.abc import BaseSchema
from fastapi_backend.typing.base import Email, JWTToken, Password
from fastapi_backend.validators.length import (
    length_str_eight_validator,
    length_str_four_validator,
)

logger = logging.getLogger("development")


valid_email = Annotated[Email, EmailStr]
valid_first_name = Annotated[str, AfterValidator(length_str_four_validator)]
valid_second_name = Annotated[str, AfterValidator(length_str_four_validator)]
valid_password = Annotated[
    Password,
    AfterValidator(length_str_eight_validator),
]


##############################################################################
# Authorization.
##############################################################################
class AuthorizationUserSchema(BaseSchema):
    """Схема для создания нового пользователя (авторизации)."""

    first_name: valid_first_name
    second_name: valid_second_name
    password: valid_password
    email: valid_email


##############################################################################
# Authentication.
##############################################################################
class CredentialsSchema(BaseSchema):
    """Схема для аутентификации пользователя по логин-паролю."""

    username: valid_email
    password: valid_password


class TokenSchema(BaseSchema):
    """Схема токена."""

    access_token: JWTToken
    token_type: str = "Bearer"
