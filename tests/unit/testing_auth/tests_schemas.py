import logging
from contextlib import nullcontext as does_not_raise

import pytest
from pydantic import ValidationError

from fastapi_backend.schemas.auth import CredentialsSchema

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    ("username", "password", "expectation"),
    [
        # Valid both.
        ("Naf-Naf24@yandex.ru", "12345678", does_not_raise()),
        ("Naf-Naf24@yandex.ru", "87654321", does_not_raise()),
        ("MarkLinz@mail.ru", "aT#12?_5", does_not_raise()),
        ("MarkLinz@mail.ru", "daw325a&5533__78adB", does_not_raise()),
        # Not valid username.
        ("Hello", "daw325a&5533__78adB", pytest.raises(ValidationError)),
        ("", "87654321", pytest.raises(ValidationError)),
        (None, "87654321", pytest.raises(ValidationError)),
        # Not valid password.
        ("Naf-Naf24@yandex.ru", "1234", pytest.raises(ValidationError)),
        ("Naf-Naf24@yandex.ru", "", pytest.raises(ValidationError)),
        ("MarkLinz@mail.ru", None, pytest.raises(ValidationError)),
    ],
)
def tests_credential_schema(username, password, expectation):
    """Schema check for password."""
    with expectation:
        filling_schema = CredentialsSchema(
            username=username,
            password=password,
        )
        assert isinstance(filling_schema, CredentialsSchema)
        data = filling_schema.model_dump()
        assert isinstance(data, dict)
        assert data["username"] == username
        assert data["password"] == password
