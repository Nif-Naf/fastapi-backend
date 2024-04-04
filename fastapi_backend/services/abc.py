from abc import ABC

from fastapi_backend.repositories.abc import AbstractRepository


class AbstractService(ABC):
    """Базовая абстракция для всех сервисов.
    В ней реализована аннотация репозитория.
    """

    _repository: AbstractRepository
