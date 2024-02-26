import logging

import pytest_asyncio
from sqlalchemy import insert

from fastapi_backend.backend.modules.password import PasswordModule
from fastapi_backend.core.connectors.postgresql import DatabaseConnector
from fastapi_backend.core.custom_type.base import Password
from fastapi_backend.core.models.abc import BaseModel
from fastapi_backend.core.models.user import UserModel

logger = logging.getLogger(__name__)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def migration() -> None:
    """Миграция в тестовую базу данных."""
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
