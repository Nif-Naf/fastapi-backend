import logging
from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

logger = logging.getLogger("dev")


class AbstractDatabaseConnector(ABC):
    """Коннектор для базы данных."""

    @abstractmethod
    def __init__(self):
        raise NotImplementedError


class SyncDatabaseConnector(AbstractDatabaseConnector):
    def __init__(self, **kwargs):
        self.engine = create_async_engine(**kwargs)

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(self.engine)


class AsyncDatabaseConnector(AbstractDatabaseConnector):
    def __init__(self, **kwargs):
        self.engine = create_engine(**kwargs)

    @property
    def session_factory(self) -> sessionmaker[Session]:
        return sessionmaker(self.engine)
