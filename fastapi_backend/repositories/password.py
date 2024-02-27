import logging

from passlib.context import CryptContext

logger = logging.getLogger("development")


class PasswordRepository:
    """Репозиторий для работы с паролями."""

    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )

    @classmethod
    def verify_password(cls, plain_password, hashed_password) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password) -> str:
        return cls.pwd_context.hash(password)
