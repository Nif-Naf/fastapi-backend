import logging

from starlette import status

from settings import VER_API_ONE
from tests.integration.client import AsyncTestingClient

logger = logging.getLogger(__name__)


class TestingIsUniqueEmail:
    client = AsyncTestingClient
    url = VER_API_ONE + "email/is_this_free/"

    async def test_unique_email(self):
        """Тестирование уникального электронного адреса."""
        response = await self.client.get(
            self.url + "LovesZebras1998@yandex.ru",
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["unique"] is True
        assert data["message"] == "This address is unique."

    async def tests_is_not_unique_email(self):
        """Тестирование не уникального электронного адреса."""
        response = await self.client.get(self.url + "GaryBirch@yandex.ru")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["unique"] is False
        assert data["message"] == "This address is not unique."
