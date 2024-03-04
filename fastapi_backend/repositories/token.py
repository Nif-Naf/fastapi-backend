from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from jose import jwt

from fastapi_backend.schemas.token import Token
from settings import ALGORITHM, EXPIRATION, SECRET_KEY


class TokenRepository:
    @classmethod
    def create(cls, email: str) -> Token:
        creation_date = datetime.now(timezone.utc)
        expiration_date = creation_date + relativedelta(**EXPIRATION)
        token = cls.encode({"sub": email, "exp": expiration_date})
        return Token(access_token=token, token_type="bearer")

    @staticmethod
    def encode(data) -> str:
        return jwt.encode(claims=data, key=SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode(token: str) -> dict[str, str | datetime]:
        return jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
