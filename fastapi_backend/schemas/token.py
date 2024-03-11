from fastapi_backend.schemas.base import BaseSchema


class Token(BaseSchema):
    access_token: str
    token_type: str
