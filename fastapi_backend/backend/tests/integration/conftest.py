import logging
from asyncio import get_event_loop_policy

import pytest
from sqlalchemy import insert

from backend.modules.password import PasswordModule
from backend.settings import SESSION_SETTINGS, SETTINGS_DB
from fastapi_backend.core.connectors.postgresql import SyncDatabaseConnector
from fastapi_backend.core.models.abc import BaseModel
from fastapi_backend.core.models.user import UserModel

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def migration() -> None:
    """Миграция в тестовую базу данных."""
    connector = SyncDatabaseConnector(**SETTINGS_DB)
    session = connector.session_factory(**SESSION_SETTINGS)
    with session as conn:
        logger.info("Delete all tables.")
        conn.run_sync(BaseModel.metadata.drop_all)
        logger.info("Create all tables.")
        conn.run_sync(BaseModel.metadata.create_all)
        logger.info("Insert two testing user into database.")
        stmt = insert(
            UserModel,
        ).values(
            [
                {
                    "first_name": "Gary",
                    "second_name": "Squirrel",
                    "email": "GaryBirch@yandex.ru",
                    "password": PasswordModule.get_hash("jump-jump-jump"),
                    "is_superuser": False,
                    "is_confirmed": False,
                    "is_deleted": False,
                },
                {
                    "first_name": "Fyr-Fyr",
                    "second_name": "Hamster",
                    "email": "Fry-Fry228@yandex.ru",
                    "password": PasswordModule.get_hash("fry-fry-fry"),
                    "is_superuser": False,
                    "is_confirmed": False,
                    "is_deleted": False,
                },
            ],
        )
        conn.execute(stmt)


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
