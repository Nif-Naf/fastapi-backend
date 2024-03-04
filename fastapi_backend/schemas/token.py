from fastapi_backend.schemas.base import BaseSchema


class TokenData(BaseSchema):
    email: str | None = None


class Token(BaseSchema):
    access_token: str
    token_type: str
