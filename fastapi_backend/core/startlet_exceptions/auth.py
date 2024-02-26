import logging

from starlette import status

from ..startlet_exceptions.abc import BaseHTTPException

logger = logging.getLogger("dev")
auth_logger = logging.getLogger("auth")


class AuthException(BaseHTTPException):
    """Базовое исключение для аутентификации."""

    ...


class TokenNotTransfer(AuthException):
    """Токен не передан."""

    message = "Token not transfer."

    def __init__(self):
        auth_logger.warning(self.message)
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=self.message,
        )


class ForbiddenExceptionFamily(AuthException):
    """Семейство исключений 403."""

    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class TokenExpiration(ForbiddenExceptionFamily):
    """Токен просрочен."""

    message = "The token has expired."

    def __init__(self):
        auth_logger.warning(self.message)
        super().__init__(detail=self.message)


class DecodeTokenFail(ForbiddenExceptionFamily):
    """Не валидный токен."""

    message = "Invalid token."

    def __init__(self):
        auth_logger.warning(self.message)
        super().__init__(detail=self.message)


class PasswordsNotMatch(ForbiddenExceptionFamily):
    """Пароль не совпал."""

    message = "Passwords did not match."

    def __init__(self):
        auth_logger.warning(self.message)
        super().__init__(detail=self.message)


class NotFoundExceptionFamily(AuthException):
    """Семейство исключений 404."""

    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class UserNotFound(NotFoundExceptionFamily):
    """Пользователь не был найден по этому логину."""

    message = "A user with this login was not found."

    def __init__(self):
        auth_logger.warning(self.message)
        super().__init__(detail=self.message)


class ConflictExceptionFamily(AuthException):
    """Семейство исключений 409."""

    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


class EmailIsNotUnique(ConflictExceptionFamily):
    """Не уникальный электронный адрес."""

    message = "This email is already in use by another user."

    def __init__(self):
        super().__init__(detail=self.message)
