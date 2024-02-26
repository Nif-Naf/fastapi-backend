import logging
from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from fastapi_backend.core.connectors.postgresql import DatabaseConnector

logger = logging.getLogger("dev")


class AbstractRepository(ABC):
    """Базовая абстракция для всех репозиториев.
    В ней реализовано подключение к базе данных. И получение сессии для
    работы с ней.
    """

    # Database.
    __database_connector = DatabaseConnector()
    _session_factory: async_sessionmaker[AsyncSession]
    _session_factory = __database_connector.session_factory
