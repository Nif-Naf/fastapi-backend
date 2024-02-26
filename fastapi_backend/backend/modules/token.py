import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from jose import jwt

from fastapi_backend.core.custom_type.base import (
    DataInJWTToken,
    Email,
    JWTToken,
)
from fastapi_backend.core.settings import ALGORITHM, EXPIRATION
from fastapi_backend.core.settings import SECRET_KEY as SECRET

logger = logging.getLogger("dev")


class AbstractTokenModule(ABC):
    """Модуль для работы с токеном."""

    @classmethod
    @abstractmethod
    def create_token(cls, email: Email) -> JWTToken:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def encode_token(data: DataInJWTToken) -> JWTToken:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def decode_token(token: JWTToken) -> DataInJWTToken:
        raise NotImplementedError


class TokenModule(AbstractTokenModule):
    @classmethod
    def create_token(cls, email: Email) -> JWTToken:
        creation_date = datetime.now(timezone.utc)
        expiration_date = creation_date + relativedelta(seconds=EXPIRATION)
        token = cls.encode_token({"sub": email, "exp": expiration_date})
        return token

    @staticmethod
    def encode_token(data: DataInJWTToken) -> JWTToken:
        token = jwt.encode(claims=data, key=SECRET, algorithm=ALGORITHM)
        return JWTToken(token)

    @staticmethod
    def decode_token(token: JWTToken) -> DataInJWTToken:
        data = jwt.decode(token=token, key=SECRET, algorithms=ALGORITHM)
        return data
