import logging

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, sessionmaker

from settings import MAIN_SETTINGS_DB, SESSION_SETTINGS

logger = logging.getLogger("development")
logger_information = logging.getLogger("information")


class NoSQLDatabaseConnector:
    """Коннектор для NoSQL БД."""

    ...


class SQLDatabaseConnector:
    """Коннектор для SQL БД."""

    def __init__(self, **kwargs):
        self.engine = create_engine(**kwargs)

    @property
    def new_session(self) -> sessionmaker[Session]:
        return sessionmaker(self.engine, **SESSION_SETTINGS)

    @staticmethod
    def create_engine(**kwargs) -> Engine:
        return create_engine(**kwargs)

    def create_tables(self) -> None:
        # logger_information.info("Creating tables")
        raise NotImplementedError

    def drop_tables(self) -> None:
        # logger_information.info("Drop tables")
        raise NotImplementedError


class PostgresDBConnector(SQLDatabaseConnector):
    """Коннектор(singleton) для СУБД: “PostgreSQL”.
    Основная база данных.
    """

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(PostgresDBConnector, cls).__new__(cls)
        return cls.instance  # noqa

    def __init__(self):
        super().__init__(**MAIN_SETTINGS_DB)
