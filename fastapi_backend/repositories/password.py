import logging

from settings import PASSWORD_CONTEXT

logger = logging.getLogger("development")


class PasswordRepository:
    """Репозиторий для работы с паролями."""

    PWD = PASSWORD_CONTEXT

    @classmethod
    def verify_password(cls, plain_password, hashed_password) -> bool:
        return cls.PWD.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password) -> str:
        return cls.PWD.hash(password)
