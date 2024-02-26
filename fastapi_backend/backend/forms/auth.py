import logging
from typing import Annotated

from fastapi.param_functions import Form

from core.schemas.auth import CredentialsSchema

logger = logging.getLogger("dev")


class OAuth2CredentialsRequestForm:
    """Форма для аутентификации по логин-паролю."""

    def __init__(
        self,
        username: Annotated[
            str,
            Form(description="Enter your login(email)."),
        ],
        password: Annotated[
            str,
            Form(min_length=8, description="Enter your password."),
        ],
    ):
        self.credentials = CredentialsSchema(
            username=username,
            password=password,
        )
