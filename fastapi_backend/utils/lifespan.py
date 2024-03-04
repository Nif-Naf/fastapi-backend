import logging
from contextlib import asynccontextmanager

from fastapi_backend.connectors.database import PostgresDBConnector
from logger_config import LogConfig
from settings import DEBUG

logger = logging.getLogger("development")


@asynccontextmanager
async def lifespan(app):
    LogConfig.init_logging_conf()
    connector = PostgresDBConnector()
    connector.create_tables() if DEBUG else ...
    yield
    # connector.drop_tables() if DEBUG else ...
