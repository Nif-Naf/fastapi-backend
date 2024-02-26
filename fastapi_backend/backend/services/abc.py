import logging
from abc import ABC

from ..repositories.abc import AbstractRepository

logger = logging.getLogger("dev")


class AbstractService(ABC):
    """Базовая абстракция для всех сервисов.
    В ней реализована аннотация репозитория.
    """

    _repository: AbstractRepository
