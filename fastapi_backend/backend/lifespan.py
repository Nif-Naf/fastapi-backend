import logging
from contextlib import asynccontextmanager

logger = logging.getLogger("dev")


@asynccontextmanager
async def lifespan(app):
    yield
