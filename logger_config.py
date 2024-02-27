from logging.config import dictConfig

from pydantic import BaseModel


class LogConfig(BaseModel):
    """Конфигурация для логирования событий."""

    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s | %(name)s - %(module)s | "
            "%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "inf": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
        },
        "test": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s | Func: %(funcName)s | Line: %(lineno)d "
            "| %(message)s",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "information": {
            "formatter": "inf",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "test": {
            "formatter": "test",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        "information": {"handlers": ["information"], "level": "INFO"},
        "production": {"handlers": ["default"], "level": "INFO"},
        "development": {"handlers": ["default"], "level": "DEBUG"},
        "testing": {"handlers": ["test"], "level": "DEBUG"},
    }

    @classmethod
    def init_logging_conf(cls) -> None:
        """Инициализация конфигурации."""
        dictConfig(cls().dict())
