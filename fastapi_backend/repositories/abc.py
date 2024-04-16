import logging
from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from fastapi_backend.connectors.database import DatabaseConnector
from fastapi_backend.connectors.queue import QueueConnector

logger = logging.getLogger("development")


class AbstractRepository(ABC):
    """Базовая абстракция для всех репозиториев.
    В ней реализовано подключение к базе данных. И получение сессии для
    работы с ней.
    """

    # Database.
    __database_connector = DatabaseConnector()
    _session_factory: async_sessionmaker[AsyncSession]
    _session_factory = __database_connector.session_factory

    # Queue.
    _queue_connector = QueueConnector()
