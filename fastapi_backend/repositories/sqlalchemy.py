import logging

from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm.session import Session, sessionmaker

from fastapi_backend.repositories.base import (
    BaseAbstractRepository,
    SchemaType,
)

logger = logging.getLogger("development")


class SqlAlchemyRepository(BaseAbstractRepository):
    """Абстракция для работы с объектами в БД через SqlAlchemy."""

    def __init__(self, session_factory: sessionmaker[Session]):
        self.__session_factory = session_factory

    def create(
        self,
        model_name: str,
        **fields_and_value,
    ) -> dict[str, SchemaType | str | None]:
        """Создать сущность."""
        model = self.get_model(model_name)
        instance = model(**fields_and_value)
        with self.__session_factory() as session:
            session.add(instance)
            try:
                session.commit()
            except DatabaseError as error:
                session.rollback()
                return {"data": None, "error": error}
            session.flush()
            schema = self.converting(instance)
            return {"data": schema, "error": None}

    def get_one(
        self,
        model_name: str,
        **filters,
    ) -> dict[str, SchemaType | str | None]:
        """Получить сущность."""
        model = self.get_model(model_name)
        with self.__session_factory() as session:
            try:
                instance = (
                    session.query(
                        model,
                    )
                    .filter_by(
                        **filters,
                    )
                    .one_or_none()
                )
            except DatabaseError as error:
                return {"data": None, "error": error}
            schema = self.converting(instance) if instance else None
            return {"data": schema, "error": None}

    def get_list(
        self,
        model_name: str,
        **filters,
    ) -> dict[str, list[SchemaType] | str | None]:
        """Получить сущности."""
        model = self.get_model(model_name)
        with self.__session_factory() as session:
            try:
                instances = (
                    session.query(
                        model,
                    )
                    .filter_by(
                        **filters,
                    )
                    .all()
                )

            except DatabaseError as error:
                return {"data": None, "error": error}
            return {"data": instances, "error": None}

    def is_exists(self, model_name, **filters) -> bool:
        """Проверка существует ли сущность."""
        model = self.get_model(model_name)
        with self.__session_factory() as session:
            return not bool(
                session.query(model).filter_by(**filters).count(),
            )
