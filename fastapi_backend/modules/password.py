import logging
from abc import ABC, abstractmethod

from passlib.context import CryptContext

from fastapi_backend.typing.base import Password, PasswordHash
from settings import PASSWORD_CONTEXT

logger = logging.getLogger("development")


class AbstractPasswordModule(ABC):
    """Модуль для работы с паролями."""

    PWD: CryptContext

    @classmethod
    @abstractmethod
    def verify_password(
        cls,
        password: Password,
        hashed_password: PasswordHash,
    ) -> bool:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_hash(cls, password: Password) -> PasswordHash:
        raise NotImplementedError


class PasswordModule(AbstractPasswordModule):
    PWD = PASSWORD_CONTEXT

    @classmethod
    def verify_password(
        cls,
        password: Password,
        hashed_password: PasswordHash,
    ) -> bool:
        return cls.PWD.verify(password, hashed_password)

    @classmethod
    def get_hash(cls, password: Password) -> PasswordHash:
        return cls.PWD.hash(password)
