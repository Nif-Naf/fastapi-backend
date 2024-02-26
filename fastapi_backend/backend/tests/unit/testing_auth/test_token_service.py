import logging
from time import sleep

import pytest
from jose import ExpiredSignatureError

from backend.modules.token import TokenModule
from backend.settings import EXPIRATION


logger = logging.getLogger(__name__)



class TestingTokenServices:
    service = TokenModule
    time_sleep = EXPIRATION + 2

    @pytest.mark.parametrize(
        "email",
        [
            "Naf-Naf24@yandex.ru",
            "MarkLinz@mail.ru",
            "",
            None,
        ],
    )
    def tests_create_token(self, email):
        """Тесты на создание токена."""
        token = self.service.create_token(email)
        assert token

    @pytest.mark.parametrize(
        "email",
        [
            "Naf-Naf24@yandex.ru",
            "MarkLinz@mail.ru",
            "",
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
            "Naf-Naf24@yandex.ru",
            "MarkLinz@mail.ru",
        ],
    )
    def tests_decode_not_fresh_token(self, email):
        """Тесты на декодирование несвежего токена."""
        valid_token = self.service.create_token(email)
        sleep(self.time_sleep)
        with pytest.raises(ExpiredSignatureError):
            self.service.decode_token(valid_token)
