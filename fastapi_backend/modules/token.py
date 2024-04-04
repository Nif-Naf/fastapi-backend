import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from jose import jwt

from fastapi_backend.typing.base import DataInJWTToken, Email, JWTToken
from settings import ALGORITHM, EXPIRATION
from settings import SECRET_KEY as SECRET

logger = logging.getLogger("development")


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
