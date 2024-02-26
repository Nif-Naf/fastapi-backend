import logging
from typing import TypedDict

from fastapi_backend.core.schemas.user import UserSchema as Schema

logger = logging.getLogger("dev")

SingleReturnType = TypedDict(
    "SingleReturnType",
    {
        "data": Schema | None,
        "error": list[str] | None,
    },
)
SeveralReturnType = TypedDict(
    "SeveralReturnType",
    {
        "data": tuple[Schema, ...] | tuple[Schema] | tuple[None],
        "error": list[str] | None,
    },
)
