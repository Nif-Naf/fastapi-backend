from abc import ABC
from typing import TypeVar

from fastapi_backend.models.user import UserModel
from fastapi_backend.schemas.user import UserWithPKScheme

ModelType = TypeVar("ModelType")
SchemaType = TypeVar("SchemaType")


class BaseAbstractRepository(ABC):
    """Базовый репозиторий для работы с ORM."""

    MAPPED_MODEL = {
        "UserModel": UserModel,
    }
    MAPPED_SCHEMA = {
        UserModel: UserWithPKScheme,
    }

    @classmethod
    def get_model(cls, model_name: str) -> ModelType:
        """Получить модель по ее имени."""
        return cls.MAPPED_MODEL[model_name]

    @classmethod
    def converting(cls, model: ModelType) -> SchemaType:
        """Конвертировать модель в схему."""
        get_scheme = cls.MAPPED_SCHEMA[model.__name__]
        filling_schema = get_scheme.model_validate(**model)
        return filling_schema
