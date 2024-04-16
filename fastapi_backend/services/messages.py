import logging
from abc import abstractmethod

from fastapi_backend.repositories.user import (
    AbstractUserRepository,
    UserRepository,
)
from fastapi_backend.schemas.response import ResponseSchema
from fastapi_backend.services.abc import AbstractService

logger = logging.getLogger("development")


class AbstractUserMessagesService(AbstractService):
    """Сервис для получения и отправки сообщений."""

    _repository: AbstractUserRepository

    @classmethod
    @abstractmethod
    def send_message(cls, user_id: int, message_body: str) -> ResponseSchema:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def receive_message(cls, user_id) -> ResponseSchema:
        raise NotImplementedError


class UserMessagesService(AbstractUserMessagesService):
    _repository = UserRepository

    @classmethod
    def send_message(cls, user_id: int, message_body: str) -> ResponseSchema:
        message = {"sender_id": user_id, "body": message_body}
        cls._repository.send_message(message=message)
        return ResponseSchema(
            data=None,
            message="You have sent a message to the queue.",
        )

    @classmethod
    def receive_message(cls, user_id: int) -> ResponseSchema:
        message = cls._repository.receive_message(user_id)
        return ResponseSchema(
            data=message,
            message="You have received a message from the queue.",
        )
