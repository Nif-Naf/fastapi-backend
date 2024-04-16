import logging
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from fastapi_backend.models.abc import BaseModel
from settings import SESSION_SETTINGS, SETTINGS_DB

logger = logging.getLogger("development")
logger_information = logging.getLogger("information")


class AbstractDatabaseConnector(ABC):
    """Коннектор для базы данных."""

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @property
    @abstractmethod
    async def session_factory(self) -> async_sessionmaker[AsyncSession]:
        raise NotImplementedError

    @abstractmethod
    async def create_tables(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def drop_tables(self) -> None:
        raise NotImplementedError


class DatabaseConnector(AbstractDatabaseConnector):
    def __init__(self):
        self.engine = create_async_engine(**SETTINGS_DB)

    @property
    def session_factory(self):
        return async_sessionmaker(self.engine, **SESSION_SETTINGS)

    async def create_tables(self) -> None:
        logger_information.info("Creating tables")
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

    async def drop_tables(self) -> None:
        logger_information.info("Drop tables")
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
