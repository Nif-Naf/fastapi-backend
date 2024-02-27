import logging

from sqlalchemy.exc import DatabaseError

from fastapi_backend.connectors.database import PostgresDBConnector
from fastapi_backend.models.user import UserModel
from fastapi_backend.schemas.user import UserSchema

logger = logging.getLogger("development")


class UserRepository:
    """Репозиторий для работы пользователем."""

    connector = PostgresDBConnector()

    @classmethod
    def create_user_repository(cls, data: UserSchema) -> dict:
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
    def email_user_is_unique(cls, email: str) -> bool:
        """Проверка на уникальность почты пользователя в рамках БД."""
        with cls.connector.new_session() as session:
            return not bool(
                session.query(UserModel)
                .filter(UserModel.email == email)
                .count(),
            )
