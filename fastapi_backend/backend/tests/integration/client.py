import logging

from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient, Client, Response, WSGITransport

from fastapi_backend.run_backend import app

logger = logging.getLogger(__name__)


class BaseTestingClient:
    _transport: WSGITransport | ASGITransport
    _client: Client | AsyncClient
    _timeout = 5

    @classmethod
    def get(cls, url: str, **kwargs: dict[str, str]) -> Response:
        raise NotImplementedError

    @classmethod
    def post(cls, url: str, **kwargs: dict[str, str]) -> Response:
        raise NotImplementedError

    @classmethod
    def patch(cls, url: str, **kwargs: dict[str, str]) -> Response:
        raise NotImplementedError

    @classmethod
    def delete(cls, url: str, **kwargs: dict[str, str]) -> Response:
        raise NotImplementedError


class SyncTestingClient(BaseTestingClient):
    """Client for API integration tests."""

    _transport = WSGITransport(app=app)
    _client = TestClient

    @classmethod
    def get(cls, url: str, **kwargs: dict[str, str]) -> Response:
        logger.info(f"Get request to: {url} with: {kwargs}")
        with cls._client(app=app) as req:
            return req.get(
                url=url,
                timeout=cls._timeout,
                **kwargs,
            )

    @classmethod
    def post(cls, url: str, **kwargs: dict[str, str]) -> Response:
        logger.info(f"Post request to: {url} with: {kwargs}")
        with cls._client(app=app) as req:
            return req.post(
                url=url,
                timeout=cls._timeout,
                **kwargs,
            )


class AsyncTestingClient(BaseTestingClient):
    """Async client for API integration tests."""

    _transport = ASGITransport(app=app)
    _client = AsyncClient

    @classmethod
    async def get(cls, url: str, **kwargs: dict[str, str]) -> Response:
        logger.info(f"Get request to: {url} with: {kwargs}")
        async with cls._client(app=app, base_url="http://testserver") as req:
            return await req.get(
                url=url,
                timeout=cls._timeout,
                **kwargs,
            )

    @classmethod
    async def post(cls, url: str, **kwargs: dict[str, str]) -> Response:
        logger.info(f"Post request to: {url} with: {kwargs}")
        async with cls._client(app=app, base_url="http://testserver") as ac:
            return await ac.post(
                url=url,
                timeout=cls._timeout,
                **kwargs,
            )

    @classmethod
    async def patch(cls, url: str, **kwargs: dict[str, str]) -> Response:
        logger.info(f"Patch request to: {url} with: {kwargs}")
        async with cls._client(app=app, base_url="http://testserver") as req:
            return await req.patch(
                url=url,
                timeout=cls._timeout,
                **kwargs,
            )

    @classmethod
    async def delete(cls, url: str, **kwargs: dict[str, str]) -> Response:
        logger.info(f"Delete request to: {url} with: {kwargs}")
        async with cls._client(app=app, base_url="http://testserver") as req:
            return await req.delete(
                url=url,
                timeout=cls._timeout,
                **kwargs,
            )
