import logging

import pytest
from starlette import status

from settings import VER_API_ONE
from tests.integration.client import AsyncTestingClient

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("nah_nah_piglet_user")
class TestingAuthorization:
    client = AsyncTestingClient
    url = VER_API_ONE + "auth/sign_up"

    async def tests_success_authorization(self, nah_nah_piglet_user):
        """Успешное создание пользователя."""
        response = await self.client.post(self.url, json=nah_nah_piglet_user)
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["data"] is None
        assert response_data["message"]
        # Checking whether the user has been created in the database.
        response_two = await self.client.post(
            self.url,
            json=nah_nah_piglet_user,
        )
        assert response_two.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.parametrize(
        ("invalid_user_data", "status_code"),
        [
            (
                {  # Case: attempt to authorization without email.
                    "first_name": "Carey",
                    "second_name": "Groundhog",
                    "email": None,
                    "password": "hide_hide_hide",
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ),
            (
                {  # Case: attempt to authorization with invalid email.
                    "first_name": "Carey",
                    "second_name": "Groundhog",
                    "email": "Fry-Fry228@=yru",
                    "password": "hide_hide_hide",
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ),
            (
                {  # Case: attempt to authorization without password.
                    "first_name": "John",
                    "second_name": "Zebra",
                    "email": "LovesZebras1998@yandex.ru",
                    "password": None,
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ),
            (
                {  # Case: attempt to authorization without non unique email.
                    "first_name": "Manatee Martin",
                    "second_name": "Manatee Martin",
                    "email": "Fry-Fry228@yandex.ru",
                    "password": "uha-uha-uha",
                },
                status.HTTP_409_CONFLICT,
            ),
        ],
    )
    async def tests_failed_authorization(self, invalid_user_data, status_code):
        """Не успешное создание пользователей."""
        response = await self.client.post(self.url, json=invalid_user_data)
        assert response.status_code == status_code
