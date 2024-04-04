import logging
from datetime import datetime
from typing import NewType, TypedDict

logger = logging.getLogger("development")

"""
Email - это новый тип данных. Представляющий из себя валидный электронный адрес
в виде строки. Например: Nif-Naf43@yandex.com

Password - это новый тип данных который представляет из себя текстовый пароль.
Который должен быть не менее 8 символов. Например: admin_admin.

PasswordHash - это новый тип данных который представляет из себя хэш текстового
пароля для сохранения в базу.

JWTToken - это новый тип данных который представляет из себя JWT токен.
DataInJWTToken - это аннотация данных(полей словаря) которые записываются и
хранятся в JWT токене.
"""
Email = NewType("Email", str)
Password = NewType("Password", str)
PasswordHash = NewType("PasswordHash", str)

JWTToken = NewType("JWTToken", str)
DataInJWTToken = TypedDict(
    "DataInJWTToken",
    {
        "sub": Email,
        "exp": datetime,
    },
)
