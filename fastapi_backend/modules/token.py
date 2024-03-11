import logging
from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from jose import jwt

from fastapi_backend.schemas.token import Token
from settings import ALGORITHM, EXPIRATION
from settings import SECRET_KEY as SECRET

logger = logging.getLogger("development")


class TokenModule:
    """Модуль для работы с паролем."""

    @classmethod
    def create_token(cls, email: str) -> Token:
        creation_date = datetime.now(timezone.utc)
        expiration_date = creation_date + relativedelta(**EXPIRATION)
        token = cls.encode_token({"sub": email, "exp": expiration_date})
        return Token(access_token=token, token_type="bearer")

    @staticmethod
    def encode_token(data) -> str:
        return jwt.encode(claims=data, key=SECRET, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict[str, str | datetime]:
        return jwt.decode(token=token, key=SECRET, algorithms=ALGORITHM)
