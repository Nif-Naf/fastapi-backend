import logging
from abc import ABC, abstractmethod

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel

from settings import QUEUE_CONNECTION_PARAMS

logger = logging.getLogger("development")


class AbstractQueueConnector(ABC):
    """Коннектор для очереди."""

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def __enter__(self) -> BlockingChannel:
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        raise NotImplementedError


class QueueConnector(AbstractQueueConnector):
    def __init__(self):
        self._connect_params = ConnectionParameters(**QUEUE_CONNECTION_PARAMS)
        self.__connection = BlockingConnection(self._connect_params)
        self.__channel = None

    def __enter__(self) -> BlockingChannel:
        self.__channel = self.__connection.channel()
        return self.__channel

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__channel.close()
        self.__connection.close()
