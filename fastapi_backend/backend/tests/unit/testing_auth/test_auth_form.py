import logging
from contextlib import nullcontext

import pytest
from pydantic import ValidationError

from backend.forms.auth import OAuth2CredentialsRequestForm

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    ("username", "password", "expectation"),
    [
        # Valid both.
        ("Naf-Naf24@yandex.ru", "12345678", nullcontext()),
        ("Naf-Naf24@yandex.ru", "87654321", nullcontext()),
        ("MarkLinz@mail.ru", "aT#12?_5", nullcontext()),
        ("MarkLinz@mail.ru", "daw325a&5533__78adB", nullcontext()),
        # Email Not valid username.
        ("Hello", "daw325a&5533__78adB", pytest.raises(ValidationError)),
        ("", "87654321", pytest.raises(ValidationError)),
        (None, "87654321", pytest.raises(ValidationError)),
        # Email Not valid password.
        ("Naf-Naf24@yandex.ru", "1234", pytest.raises(ValidationError)),
        ("Naf-Naf24@yandex.ru", "", pytest.raises(ValidationError)),
        ("MarkLinz@mail.ru", None, pytest.raises(ValidationError)),
    ],
)
def tests_credential_schema(username, password, expectation):
    """Проверка схемы на валидность данных для аутентификации."""
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
