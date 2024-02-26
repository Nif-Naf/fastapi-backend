import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any

from dateutil.relativedelta import relativedelta
from jose import jwt

from ..settings import ALGORITHM, EXPIRATION, SECRET_KEY

logger = logging.getLogger("dev")


class AbstractTokenModule(ABC):
    """Модуль для работы с токеном."""

    @classmethod
    @abstractmethod
    def create_token(cls, email: str) -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def encode_token(data: dict[str, Any]) -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def decode_token(token: str) -> dict[str, Any]:
        raise NotImplementedError


class TokenModule(AbstractTokenModule):
    @classmethod
    def create_token(cls, email: str) -> str:
        creation_date = datetime.now(timezone.utc)
        expiration_date = creation_date + relativedelta(seconds=EXPIRATION)
        token = cls.encode_token({"sub": email, "exp": expiration_date})
        return token

    @staticmethod
    def encode_token(data: dict[str, Any]) -> str:
        token = jwt.encode(claims=data, key=SECRET_KEY, algorithm=ALGORITHM)
        return token

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        data = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        return data
