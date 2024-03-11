from fastapi import HTTPException
from starlette import status


class AuthException(HTTPException):
    """Базовое исключение для аутентификации."""

    def __init__(self, status_code, detail):
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenNotTransfer(AuthException):
    """Исключение: Токен не передан."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not transfer.",
        )


class TokenExpiration(AuthException):
    """Исключение: Токен просрочен."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The token has expired.",
        )


class DecodeTokenFail(AuthException):
    """Исключение: Не корректный токен."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token.",
        )


class UserNotFound(AuthException):
    """Исключение: По данному логину не удалось найти пользователя."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="A user with this login was not found.",
        )


class PasswordsNotMatch(AuthException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Passwords did not match.",
        )
