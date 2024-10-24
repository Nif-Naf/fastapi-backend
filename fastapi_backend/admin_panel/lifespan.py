from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app):
    yield
