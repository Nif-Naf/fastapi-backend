import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.fixture(scope="package")
def nah_nah_piglet_user() -> dict:
    """Валидные данные тестового пользователя: поросенка Нах-Нах."""
    return {
        "first_name": "Nah-Nah",
        "second_name": "Piglet",
        "email": "Hru-Hru2024@yandex.ru",
        "password": "hru-hru-hru",
    }
