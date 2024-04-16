import json
import logging
from abc import abstractmethod
from typing import Sequence, TypedDict

from pika.exchange_type import ExchangeType
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError

from fastapi_backend.models.user import UserModel as Model
from fastapi_backend.repositories.abc import AbstractRepository
from fastapi_backend.schemas.auth import AuthorizationUserSchema
from fastapi_backend.schemas.user import UserSchema as Schema
from fastapi_backend.typing.base import Message

logger = logging.getLogger("development")

##############################################################################
# Typing.
##############################################################################
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


##############################################################################
# Abstraction.
##############################################################################
class AbstractUserRepository(AbstractRepository):
    """Репозиторий для работы с пользователями в БД."""

    queue: str

    @classmethod
    @abstractmethod
    async def send_message(cls, message: Message) -> None:
        """Отправить сообщение через очередь."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def receive_message(cls, user_id: int) -> dict:
        """Получить сообщение через очередь."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def create(cls, schema: AuthorizationUserSchema) -> SingleReturnType:
        """Создание пользователя в базе данных."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def find_one(cls, **fields) -> SingleReturnType:
        """Найти одного пользователя."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def find_several(cls, **fields) -> SeveralReturnType:
        """Найти несколько пользователей."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def is_exists(cls, **fields) -> bool:
        """Проверка существует ли пользователь с такими полями."""
        raise NotImplementedError

    @classmethod
    async def model_to_schema(cls, model: Model | None) -> Schema | None:
        """Преобразование модели в схему."""
        if model is None:
            return None
        try:
            return Schema.model_validate(model, from_attributes=True)
        except ValidationError as e:
            error = e.errors()
            raise Warning(
                f"Validation Error into 'model_to_schema'. Errors: {error}",
            )

    @classmethod
    async def models_to_schemas(
        cls,
        *models: Sequence[Model] | Sequence[None],
    ) -> tuple[Schema, ...]:
        """Преобразование моделей в схемы."""
        schemas = []
        try:
            for model in models:
                schema = Schema.model_validate(model, from_attributes=True)
                schemas.append(schema)
            return tuple(schemas)
        except ValidationError as e:
            error = e.errors()
            raise Warning(
                f"Validation Error into 'models_to_schemas'. Errors: {error}",
            )

    @classmethod
    async def schema_to_model(cls, schema: AuthorizationUserSchema) -> Model:
        """Преобразование схемы в модель."""
        fields = Schema.model_dump(schema)
        return Model(**fields)


##############################################################################
# Realisation.
##############################################################################
class UserRepository(AbstractUserRepository):
    queue = "user_messages"
    exchange = "user_exchange"
    exchange_type = ExchangeType.direct

    @classmethod
    def send_message(cls, message: Message) -> None:
        """Добавить сообщение в очередь."""
        json_message = json.dumps(message)
        with cls._queue_connector as channel:
            channel.exchange_declare(cls.exchange, cls.exchange_type)
            channel.basic_publish(cls.exchange, cls.queue, json_message)
            logger.debug(
                f"User: {message['sender_id']} send: {message['body']}"
            )

    @classmethod
    def receive_message(cls, user_id: int) -> Message | None:
        """Получить сообщение из очереди."""
        message = None

        def callback(ch, method, properties, body) -> None:  # noqa
            nonlocal message
            message = body

        with cls._queue_connector as channel:
            channel.exchange_declare(cls.exchange, cls.exchange_type)
            user_queue = channel.queue_declare(queue=cls.queue)
            channel.queue_bind(
                exchange=cls.exchange,
                queue=user_queue.method.queue,
                routing_key=cls.queue,
            )
            channel.basic_consume(
                queue=user_queue.method.queue,
                on_message_callback=callback,
                auto_ack=True,
            )
            channel.start_consuming()
            logger.debug(f"User: {user_id} receive message")
            return message

    @classmethod
    async def create(cls, schema) -> SingleReturnType:
        model = await cls.schema_to_model(schema)
        async with cls._session_factory() as session:
            session.add(model)
            await session.flush((model,))  # Send data to DB.
            try:
                await session.commit()  # Commited data to DB.
            except DatabaseError as error:
                await session.rollback()
                return {"data": None, "error": error.detail}
            return {"data": await cls.model_to_schema(model), "error": None}

    @classmethod
    async def find_one(cls, **filters) -> SingleReturnType:
        query = select(Model).filter_by(**filters)
        async with cls._session_factory() as session:
            try:
                result = await session.scalars(query)
            except DatabaseError as error:
                return {"data": None, "error": error.detail}
            user = result.one_or_none()
            return {"data": await cls.model_to_schema(user), "error": None}

    @classmethod
    async def find_several(cls, **filters) -> SeveralReturnType:
        query = select(Model).filter_by(**filters)
        async with cls._session_factory() as session:
            try:
                result = await session.execute(query)
            except DatabaseError as error:
                return {"data": tuple(...), "error": error.detail}
            users = result.scalars().all()
            return {"data": await cls.models_to_schemas(users), "error": None}

    @classmethod
    async def is_exists(cls, **filters) -> bool:
        query = select(Model).filter_by(**filters)
        async with cls._session_factory() as session:
            result = await session.execute(query)
            return not bool(result.scalar())
