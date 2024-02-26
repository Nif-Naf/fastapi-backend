import os

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

RABBIT_HOST = os.getenv("RABBIT_HOST")
RABBIT_PORT = os.getenv("RABBIT_PORT")
RABIT_SETTINGS = {
    "host": RABBIT_HOST,
    "port": RABBIT_PORT,
}

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

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
