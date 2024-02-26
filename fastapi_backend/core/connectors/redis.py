import logging
from abc import ABC, abstractmethod

from aioredis import Redis as AsyncRedis
from redis import Redis as SyncRedis

dev_logger = logging.getLogger("dev")

__all__ = (
    "SyncRedisConnector",
    "AsyncRedisConnector",
)


class AbstractRedisConnector(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError


class SyncRedisConnector:
    def __init__(self, **kwargs):
        self.conn = SyncRedis(**kwargs)

    def __enter__(self) -> SyncRedis:
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.close()


class AsyncRedisConnector:
    def __init__(self, **kwargs):
        self.coro_conn = AsyncRedis.from_url(**kwargs)

    async def __aenter__(self) -> AsyncRedis:
        return await self.coro_conn

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.coro_conn.close()
