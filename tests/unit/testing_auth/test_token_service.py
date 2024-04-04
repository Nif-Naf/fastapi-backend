import logging
import os
from time import sleep

import pytest
from jose import ExpiredSignatureError

from fastapi_backend.modules.token import TokenModule
from fastapi_backend.typing.base import Email

logger = logging.getLogger(__name__)


class TestingTokenServices:
    service = TokenModule
    time_sleep = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS")) + 2

    @pytest.mark.parametrize(
        "email",
        [
            Email("Naf-Naf24@yandex.ru"),
            Email("MarkLinz@mail.ru"),
            Email(""),
            Email(None),
        ],
    )
    def tests_create_token(self, email):
        """Тесты на создание токена."""
        token = self.service.create_token(email)
        assert token

    @pytest.mark.parametrize(
        "email",
        [
            Email("Naf-Naf24@yandex.ru"),
            Email("MarkLinz@mail.ru"),
            Email(""),
        ],
    )
    def tests_success_decode_token(self, email):
        """Проверка на успешность декодирования токена."""
        valid_token = self.service.create_token(email)
        data_in_token = self.service.decode_token(valid_token)
        sub, exp = data_in_token["sub"], data_in_token["exp"]
        assert isinstance(sub, str)
        assert sub == email
        assert isinstance(exp, int)

    @pytest.mark.parametrize(
        "email",
        [
            Email("Naf-Naf24@yandex.ru"),
            Email("MarkLinz@mail.ru"),
        ],
    )
    def tests_decode_not_fresh_token(self, email):
        """Тесты на декодирование несвежего токена."""
        valid_token = self.service.create_token(email)
        sleep(self.time_sleep)
        with pytest.raises(ExpiredSignatureError):
            self.service.decode_token(valid_token)
