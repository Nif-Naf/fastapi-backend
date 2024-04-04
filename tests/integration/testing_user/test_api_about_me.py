import logging

import pytest
from starlette import status

from settings import TOKEN_TYPE, VER_API_ONE
from tests.integration.client import AsyncTestingClient

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("squirrel_credentials")
class TestingAboutMe:
    client = AsyncTestingClient
    url = VER_API_ONE + "user/about_me/"

    async def test_info_about_me(self, squirrel_credentials):
        """Тестирование получение информации обо мне. С помощью
        аутентификации по токену.
        """
        # Получение токена.
        receive_token_response = await self.client.post(
            url=VER_API_ONE + "auth/login",
            data=squirrel_credentials,
        )
        assert receive_token_response.status_code == status.HTTP_200_OK
        headers_credentials = receive_token_response.json()
        logger.info(f"Response: {headers_credentials}")
        access_token = headers_credentials["access_token"]
        token_type = headers_credentials["token_type"]
        assert access_token
        assert token_type == TOKEN_TYPE
        # Получение информации о пользователе.
        receive_user_data = await self.client.get(
            url=VER_API_ONE + "user/about_me",
            headers={"Authorization": f"{token_type} {access_token}"},
        )
        response = receive_user_data.json()
        logger.info(f"Response: {response}")
        user_fields = response["data"]
        message = response["message"]
        assert user_fields
        assert isinstance(user_fields, dict)
        assert message
        assert isinstance(message, str)
        assert user_fields["id"]
        assert isinstance(user_fields["id"], int)
        assert user_fields["first_name"] == "Gary"
        assert user_fields["second_name"] == "Squirrel"
        assert user_fields["email"] == "GaryBirch@yandex.ru"
        assert user_fields["password"]
        assert user_fields["created_at"]
        assert user_fields["updated_at"]
