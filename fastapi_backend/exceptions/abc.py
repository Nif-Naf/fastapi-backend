from typing import Any

from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    """Базовое исключение."""

    description = "Not definitely."

    def __init__(self, status_code: int, detail: str):
        super().__init__(
            status_code=status_code,
            detail=detail,
        )

    def return_doc(self) -> dict[int, dict[str, Any]]:
        """Метод, который возвращает ответ для swagger."""
        return {
            self.status_code: {
                "description": self.description,
                "content": {
                    "application/json": {
                        "example": {
                            "detail": self.detail,
                        },
                    },
                },
            },
        }
