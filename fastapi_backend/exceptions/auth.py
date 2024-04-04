from starlette import status

from fastapi_backend.exceptions.abc import BaseHTTPException


class AuthException(BaseHTTPException):
    """Базовое исключение для аутентификации."""

    ...


class TokenNotTransfer(AuthException):
    """Токен не передан."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not transfer.",
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

    def __init__(self):
        super().__init__(
            detail="The token has expired.",
        )


class DecodeTokenFail(ForbiddenExceptionFamily):
    """Не валидный токен."""

    def __init__(self):
        super().__init__(
            detail="Invalid token.",
        )


class PasswordsNotMatch(ForbiddenExceptionFamily):
    """Пароль не совпал."""

    def __init__(self):
        super().__init__(
            detail="Passwords did not match.",
        )


class NotFoundExceptionFamily(AuthException):
    """Семейство исключений 404."""

    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class UserNotFound(NotFoundExceptionFamily):
    """Пользователь не был найден по этому логину."""

    def __init__(self):
        super().__init__(
            detail="A user with this login was not found.",
        )


class ConflictExceptionFamily(AuthException):
    """Семейство исключений 409."""

    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


class EmailIsNotUnique(ConflictExceptionFamily):
    """Не уникальный электронный адрес."""

    def __init__(self):
        super().__init__(
            detail="This email is already in use by another user.",
        )
