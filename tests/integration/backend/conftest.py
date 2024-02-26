import logging
from asyncio import get_event_loop_policy

import pytest

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def event_loop():
    """Создание экземпляра цикла событий по умолчанию для каждого тестового
     примера.

    Если его нет, то возникнут следующие исключения:
        - InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>:
        cannot perform operation: another operation is in progress
        - RuntimeError: Task ... running at ... got Future ... attached to a
        different loop
    """
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="package")
def squirrel_credentials() -> dict:
    """Валидные логин-пароль тестового пользователя: белки Гарри."""
    return {
        "username": "GaryBirch@yandex.ru",
        "password": "jump-jump-jump",
    }


@pytest.fixture(scope="package")
def hamster_credentials() -> dict:
    """Валидные логин-пароль тестового пользователя: хомячка Фыр-Фыр."""
    return {
        "username": "Fry-Fry228@yandex.ru",
        "password": "fry-fry-fry",
    }
