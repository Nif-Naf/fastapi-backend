import logging

from starlette import status

from ..startlet_exceptions.abc import BaseHTTPException

logger = logging.getLogger("dev")


class CommonException(BaseHTTPException):
    """Базовое общее исключение."""

    def __init__(self, status_code, detail):
        super().__init__(
            status_code=status_code,
            detail=detail,
        )


class DataBaseUnknownError(CommonException):
    """Универсальная общая ошибка связанная с БД."""

    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )
