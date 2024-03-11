from fastapi_backend.connectors.database import PostgresDBConnector
from fastapi_backend.repositories.sqlalchemy import SqlAlchemyRepository


class BaseService:
    """Базовый сервис.
    Инкапсулирует дефолтное подключение к низкоуровневым модулям.
    """

    def __init__(
        self,
        connector=PostgresDBConnector,
        orm=SqlAlchemyRepository,
    ):
        self.connector = connector()
        self.orm = orm(self.connector.session_factory)
