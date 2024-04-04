import logging
from contextlib import nullcontext as does_not_raise

import pytest

from fastapi_backend.modules.password import PasswordModule
from fastapi_backend.typing.base import Password

logger = logging.getLogger(__name__)


class TestingPasswordService:
    service = PasswordModule

    @pytest.mark.parametrize(
        ("password", "expectation"),
        [
            (Password("12345678"), does_not_raise()),
            (Password("87654321"), does_not_raise()),
            (Password("aT#12?_5"), does_not_raise()),
            (Password("daw325a&5533__78adB"), does_not_raise()),
            (Password("1234"), does_not_raise()),
            (Password(""), does_not_raise()),
            (Password(12), pytest.raises(TypeError)),
            (Password(None), pytest.raises(TypeError)),
        ],
    )
    def tests_create_new_password(self, password, expectation):
        """Тесты на создание хэш-пароля."""
        with expectation:
            hash_password = self.service.get_hash(password)
            assert hash_password

    @pytest.mark.parametrize(
        ("password", "const"),
        [
            (Password("12345678"), Password("12345678")),
            (Password("87654321"), Password("87654321")),
            (Password("aT#12?_5"), Password("aT#12?_5")),
            (Password("daw325a&5533__78adB"), Password("daw325a&5533__78adB")),
        ],
    )
    def tests_success_verify_password(self, password, const):
        """Тесты на совпадение двух паролей."""
        password_hash = self.service.get_hash(password)
        is_match = self.service.verify_password(const, password_hash)
        assert is_match

    @pytest.mark.parametrize(
        ("password", "const"),
        [
            (Password("admin"), Password("user")),
            (Password("qwerty_21"), Password("21_qwerty")),
            (Password("daw325a&5533__78adB"), Password("daw325_78adB")),
        ],
    )
    def tests_fail_verify_password(self, password, const):
        """Тесты на не совпадение двух паролей."""
        password_hash = self.service.get_hash(password)
        is_match = self.service.verify_password(const, password_hash)
        assert not is_match
