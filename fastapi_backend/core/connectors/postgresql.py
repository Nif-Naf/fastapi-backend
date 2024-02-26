import logging
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ..settings import SESSION_SETTINGS, SETTINGS_DB

logger = logging.getLogger("dev")


class AbstractDatabaseConnector(ABC):
    """Коннектор для базы данных."""

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @property
    @abstractmethod
    async def session_factory(self) -> async_sessionmaker[AsyncSession]:
        raise NotImplementedError


class DatabaseConnector(AbstractDatabaseConnector):
    def __init__(self):
        self.engine = create_async_engine(**SETTINGS_DB)

    @property
    def session_factory(self):
        return async_sessionmaker(self.engine, **SESSION_SETTINGS)
