import logging
from typing import Annotated

from fastapi import Depends
from jose import JWTError
from pydantic_core import ValidationError
from sqlalchemy.exc import DatabaseError
from starlette import status
from starlette.exceptions import HTTPException

from fastapi_backend.connectors.database import PostgresDBConnector
from fastapi_backend.models.user import UserModel
from fastapi_backend.repositories.token import TokenRepository
from fastapi_backend.schemas.user import UserSchema, UserWithPKScheme
from settings import OAUTH2_SCHEME

logger = logging.getLogger("development")


class UserRepository:
    """Репозиторий для работы пользователем."""

    connector = PostgresDBConnector()

    @classmethod
    def email_user_is_unique(cls, email: str) -> bool:
        """Проверка на уникальность почты пользователя в рамках БД."""
        with cls.connector.new_session() as session:
            return not bool(
                session.query(UserModel).filter_by(email=email).count(),
            )

    @classmethod
    def create_user(cls, data: UserSchema) -> dict:
        """Создание нового пользователя."""
        with cls.connector.new_session() as session:
            kwargs = data.model_dump()
            instance = UserModel(**kwargs)
            session.add(instance)
            try:
                session.commit()
            except DatabaseError as error:
                session.rollback()
                logger.error(f"Create user error. Rollback. Error: {error}")
                return {"error": error}
            return {"error": None}

    @classmethod
    def find_user(cls, **kwargs) -> dict:
        """Поиск пользователя в БД по заданным фильтрам.

        Keyword Args:
            name (str) - Имя пользователя.
            username (str) - Псевдоним пользователя.
            email (str) - Почта пользователя.
        """

        with cls.connector.new_session() as session:
            user_model: UserModel | None = (
                session.query(UserModel).filter_by(**kwargs).one_or_none()
            )
            logger.debug(f"User Model in DB: {user_model}")
            if user_model is None:
                return {"data": None, "error": "User not found"}
            try:
                user_schema = UserWithPKScheme(
                    id=user_model.id,
                    name=user_model.name,
                    username=user_model.username,
                    email=user_model.email,
                    password=user_model.password,
                )
            except ValidationError as error:
                logger.error(error)
                return {"data": None, "error": str(error)}
            return {"data": user_schema, "error": None}

    @classmethod
    def get_current_user(
        cls,
        token: Annotated[str, Depends(OAUTH2_SCHEME)],
    ) -> UserWithPKScheme:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        print(token)
        try:
            email, _ = TokenRepository.decode(token).values()
        except JWTError as error:
            logger.error(f"JWTError: {error}")
            raise credentials_exception
        if email is None:
            logger.error(f"Email is {email}")
            raise credentials_exception
        user, error = cls.find_user(email=email).values()
        if user is None:
            logger.error(f"User is {email}")
            raise credentials_exception
        return user
