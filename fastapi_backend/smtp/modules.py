import logging
import smtplib
from typing import Any

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from sqlalchemy import create_engine, select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker

from ..core.models import UserModel
from ..core.models.logs import SMTPLogModel
from .settings import (
    ALGORITHM,
    MAIL_PASSWORD,
    MAIL_USERNAME,
    SECRET_KEY,
    SESSION_SETTINGS,
    SETTINGS_DB,
)

logger = logging.getLogger(__name__)

ENGINE = create_engine(**SETTINGS_DB)
SESSION = sessionmaker(bind=ENGINE, **SESSION_SETTINGS)


def send_email(self, subject, body, to_email):
    """Функция для отправки сообщения."""
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(MAIL_USERNAME, to_email, message)


def decode_token(token: str) -> dict[str, Any]:
    """Простая функция аутентификации пользователя для SMTP приложения."""
    if not token:
        logger.debug("Токен отсутствует.")
        logger.exception("Аутентификация провалена.")
    try:
        return jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
    except ExpiredSignatureError:
        logger.debug("Токен просрочен.")
        logger.exception("Аутентификация провалена.")
    except JWTError:
        logger.debug("Токен не возможно расшифровать.")
        logger.exception("Аутентификация провалена.")


def get_user(email: str):
    with SESSION() as session:
        query = select(UserModel).filter_by(email=email)
        result = session.execute(query)
        user = result.scalars().one_or_none()
        return user


def create_user_log(**kwargs):
    with SESSION() as session:
        log = SMTPLogModel(**kwargs)
        session.add(log)
        try:
            session.commit()
        except DatabaseError:
            session.rollback()
            logger.exception("Error write log.")
