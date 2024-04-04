from typing import Annotated

from fastapi.param_functions import Form

from fastapi_backend.schemas.auth import CredentialsSchema
from fastapi_backend.typing.base import Email, Password


class OAuth2CredentialsRequestForm:
    """Форма для аутентификации по логин-паролю."""

    def __init__(
        self,
        username: Annotated[
            Email,
            Form(description="Enter your login(email)."),
        ],
        password: Annotated[
            Password,
            Form(min_length=8, description="Enter your password."),
        ],
    ):
        self.credentials = CredentialsSchema(
            username=username,
            password=password,
        )
