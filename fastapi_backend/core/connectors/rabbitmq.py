import logging
from abc import ABC, abstractmethod
from typing import Optional

from pika.adapters.blocking_connection import (
    BlockingChannel,
    BlockingConnection,
)
from pika.connection import ConnectionParameters

logger = logging.getLogger("dev")


class AbstractQueueConnector(ABC):
    """Коннектор для очередей."""

    def __init__(self, **kwargs):
        self.connection = BlockingConnection(ConnectionParameters(**kwargs))

    @property
    @abstractmethod
    async def channel(self, **kwargs) -> BlockingChannel:
        raise NotImplementedError


class QueueConnector(AbstractQueueConnector):
    queue = {
        "email": "email_queue",  # Send email notification.
        "auth": "auth_queue",  # Token verification.
    }

    @property
    def channel(self, **kwargs):
        return self.connection.channel()

    def name_of_queue(self, name: str) -> Optional[str]:
        return self.queue.get(name)
