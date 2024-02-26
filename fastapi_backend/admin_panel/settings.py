import os
from typing import Literal

ADMIN_HOST = os.getenv("ADMIN_HOST")
ADMIN_PORT = int(os.getenv("ADMIN_PORT"))
ADMIN_DEBUG = bool(os.getenv("ADMIN_DEBUG"))
ADMIN_LOG_LEVEL = os.getenv("ADMIN_LOG_LEVEL")
ADMIN_RELOAD = bool(os.getenv("ADMIN_AUTO_RELOAD"))

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

# Redis databases and what they store:
# 0 - Not used.
# 1 - Not used.
# 2 - Not used.
# ...
# 10 - Not used.
# 11 - Not used.
FREE_REDIS_DATABASES = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

ADMIN_OFF_AUTH = True if os.getenv("ADMIN_OFF_AUTH") == "True" else False

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:"
    f"{DB_PORT}/{DB_NAME}"
)

ECHO = True if os.getenv("DB_ECHO") == "True" else False

SETTINGS_DB = {
    "url": DATABASE_URL,
    "echo": ECHO,
}

SESSION_SETTINGS = {
    "autocommit": False,
    "autoflush": False,
    "expire_on_commit": False,
}
