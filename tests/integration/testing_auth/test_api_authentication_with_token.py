import logging
import os
from asyncio import sleep

import pytest
from starlette import status

from fastapi_backend.exceptions.auth import TokenExpiration
from fastapi_backend.services.authentication import AuthenticationService
from settings import TOKEN_TYPE, VER_API_ONE
from tests.integration.client import AsyncTestingClient

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("squirrel_credentials")
class TestingTokenAuthentication:
    client = AsyncTestingClient
    url = VER_API_ONE + "auth/login"
    time_sleep = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS")) + 2

    async def tests_success_authentication(self, squirrel_credentials):
        """Успешная аутентификация пользователя по токену."""
        receive_token_response = await self.client.post(
            url=self.url,
            data=squirrel_credentials,
        )
        assert receive_token_response.status_code == status.HTTP_200_OK
        headers_credentials = receive_token_response.json()
        access_token = headers_credentials["access_token"]
        assert access_token
        assert headers_credentials["token_type"] == TOKEN_TYPE
        user = await AuthenticationService.with_token(token=access_token)
        assert user.first_name == "Gary"
        assert user.second_name == "Squirrel"
        assert user.email == "GaryBirch@yandex.ru"

    async def tests_authentication_with_old_token(self, squirrel_credentials):
        """Попытка аутентификации пользователя по просроченному токену."""
        receive_token_response = await self.client.post(
            url=self.url,
            data=squirrel_credentials,
        )
        assert receive_token_response.status_code == status.HTTP_200_OK
        headers_credentials = receive_token_response.json()
        access_token = headers_credentials["access_token"]
        assert access_token
        assert headers_credentials["token_type"] == TOKEN_TYPE
        await sleep(self.time_sleep)
        with pytest.raises(TokenExpiration):
            await AuthenticationService.with_token(token=access_token)
