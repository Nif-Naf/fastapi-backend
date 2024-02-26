import logging
from contextlib import nullcontext as does_not_raise

import pytest

from backend.modules.password import PasswordModule

logger = logging.getLogger(__name__)


class TestingPasswordService:
    service = PasswordModule

    @pytest.mark.parametrize(
        ("password", "expectation"),
        [
            ("12345678", does_not_raise()),
            ("87654321", does_not_raise()),
            ("aT#12?_5", does_not_raise()),
            ("daw325a&5533__78adB", does_not_raise()),
            ("1234", does_not_raise()),
            ("", does_not_raise()),
            (12, pytest.raises(TypeError)),
            (None, pytest.raises(TypeError)),
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
            ("12345678", "12345678"),
            ("87654321", "87654321"),
            ("aT#12?_5", "aT#12?_5"),
            ("daw325a&5533__78adB", "daw325a&5533__78adB"),
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
            ("admin", "user"),
            ("qwerty_21", "21_qwerty"),
            ("daw325a&5533__78adB", "daw325_78adB"),
        ],
    )
    def tests_fail_verify_password(self, password, const):
        """Тесты на не совпадение двух паролей."""
        password_hash = self.service.get_hash(password)
        is_match = self.service.verify_password(const, password_hash)
        assert not is_match
