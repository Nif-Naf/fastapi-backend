import logging
from asyncio import get_event_loop_policy

import pytest
import pytest_asyncio
from sqlalchemy import insert

from fastapi_backend.connectors.database import DatabaseConnector
from fastapi_backend.models.abc import BaseModel
from fastapi_backend.models.user import UserModel
from fastapi_backend.modules.password import PasswordModule
from fastapi_backend.typing.base import Password

logger = logging.getLogger(__name__)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def migration() -> None:
    """Миграция в базу данных."""
    connector = DatabaseConnector()
    engine = connector.engine
    async with engine.begin() as conn:
        logger.info("Delete all tables.")
        await conn.run_sync(BaseModel.metadata.drop_all)
        logger.info("Create all tables.")
        await conn.run_sync(BaseModel.metadata.create_all)
        logger.info("Insert two testing user into database.")
        stmt = insert(
            UserModel,
        ).values(
            [
                {
                    "first_name": "Gary",
                    "second_name": "Squirrel",
                    "email": "GaryBirch@yandex.ru",
                    "password": PasswordModule.get_hash(
                        Password("jump-jump-jump"),
                    ),
                },
                {
                    "first_name": "Fyr-Fyr",
                    "second_name": "Hamster",
                    "email": "Fry-Fry228@yandex.ru",
                    "password": PasswordModule.get_hash(
                        Password("fry-fry-fry"),
                    ),
                },
            ],
        )
        await conn.execute(stmt)


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
