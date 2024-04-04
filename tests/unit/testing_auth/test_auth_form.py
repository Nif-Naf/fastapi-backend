import logging
from contextlib import nullcontext as d_n_r

import pytest
from pydantic import ValidationError as ValEr

from fastapi_backend.form.auth import OAuth2CredentialsRequestForm
from fastapi_backend.typing.base import Email, Password

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    ("username", "password", "expectation"),
    [
        # Valid both.
        (Email("Naf-Naf24@yandex.ru"), Password("12345678"), d_n_r()),
        (Email("Naf-Naf24@yandex.ru"), Password("87654321"), d_n_r()),
        (Email("MarkLinz@mail.ru"), Password("aT#12?_5"), d_n_r()),
        (Email("MarkLinz@mail.ru"), Password("daw325a&5533__78adB"), d_n_r()),
        # Email Not valid username.
        (
            Email("Hello"),
            Password("daw325a&5533__78adB"),
            pytest.raises(ValEr),
        ),
        (Email(""), Password("87654321"), pytest.raises(ValEr)),
        (Email(None), Password("87654321"), pytest.raises(ValEr)),
        # Email Not valid password.
        (Email("Naf-Naf24@yandex.ru"), Password("1234"), pytest.raises(ValEr)),
        (Email("Naf-Naf24@yandex.ru"), Password(""), pytest.raises(ValEr)),
        (Email("MarkLinz@mail.ru"), Password(None), pytest.raises(ValEr)),
    ],
)
def tests_credential_schema(username, password, expectation):
    """Schema check for password."""
    with expectation:
        filling_form = OAuth2CredentialsRequestForm(
            username=username,
            password=password,
        )
        assert isinstance(filling_form, OAuth2CredentialsRequestForm)
        credentials = filling_form.credentials.model_dump()
        assert isinstance(credentials, dict)
        assert credentials["username"] == username
        assert credentials["password"] == password
