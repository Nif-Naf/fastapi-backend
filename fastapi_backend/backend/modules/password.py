import logging
from abc import ABC, abstractmethod

from passlib.context import CryptContext

from backend.settings import PASSWORD_CONTEXT

logger = logging.getLogger("dev")


class AbstractPasswordModule(ABC):
    """Модуль для работы с паролями."""

    PWD: CryptContext

    @classmethod
    @abstractmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_hash(cls, password: str) -> str:
        raise NotImplementedError


class PasswordModule(AbstractPasswordModule):
    PWD = PASSWORD_CONTEXT

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        return cls.PWD.verify(password, hashed_password)

    @classmethod
    def get_hash(cls, password: str) -> str:
        return cls.PWD.hash(password)
