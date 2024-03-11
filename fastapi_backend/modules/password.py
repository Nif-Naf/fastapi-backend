import logging

from settings import PASSWORD_CONTEXT

logger = logging.getLogger("development")


class PasswordModule:
    """Модуль для работы с паролями."""

    PWD = PASSWORD_CONTEXT

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        return cls.PWD.verify(password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.PWD.hash(password)
