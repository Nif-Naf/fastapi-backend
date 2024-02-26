import logging

import pytest
from starlette import status

from backend.settings import TOKEN_TYPE, VER_API_ONE
from backend.tests.integration.client import AsyncTestingClient

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("hamster_credentials")
class TestingSimpleCredentialsAuthentication:
    client = AsyncTestingClient
    url = VER_API_ONE + "auth/login"

    async def tests_success_authentication(self, hamster_credentials):
        """Тестирование аутентификации с валидными данными пользователя."""
        receive_token_response = await self.client.post(
            url=self.url,
            data=hamster_credentials,
        )
        assert receive_token_response.status_code == status.HTTP_200_OK
        headers_credentials = receive_token_response.json()
        access_token = headers_credentials["access_token"]
        assert access_token
        assert headers_credentials["token_type"] == TOKEN_TYPE

    @pytest.mark.parametrize(
        ("user_data", "http_status_code"),
        [
            (
                {  # Case: attempt to authentication without email.
                    "username": None,
                    "password": "fyr-fyr-fyr",
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ),
            (
                {  # Case: attempt to authentication  with wrong email.
                    "username": "LovesZebras1998@yandex.ru",
                    "password": "fyr-fyr-fyr",
                },
                status.HTTP_404_NOT_FOUND,
            ),
            (
                {  # Case: attempt to authenticate with someone else's email.
                    "username": "GaryBirch@yandex.ru",
                    "password": "fyr-fyr-fyr",
                },
                status.HTTP_403_FORBIDDEN,
            ),
            (
                {  # Case: attempt to authentication without password.
                    "username": "Fry-Fry228@yandex.ru",
                    "password": None,
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ),
            (
                {  # Case: attempt to authentication with wrong password.
                    "username": "Fry-Fry228@yandex.ru",
                    "password": "for-for-for",
                },
                status.HTTP_403_FORBIDDEN,
            ),
            (
                {
                    # Case: attempt to authenticate with someone else's pass.
                    "username": "Fry-Fry228@yandex.ru",
                    "password": "jump-jump-jump",
                },
                status.HTTP_403_FORBIDDEN,
            ),
        ],
    )
    async def tests_failed_authorization(self, user_data, http_status_code):
        """Тестирование аутентификации с невалидными данными пользователя."""
        response = await self.client.post(url=self.url, data=user_data)
        assert response.status_code == http_status_code
