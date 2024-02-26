import os

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from fastapi_backend.core.settings_func import (
    load_logger_config,
    loads_envs_files,
)

load_logger_config()
loads_envs_files()

# Project settings.
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
DEBUG = bool(os.getenv("DEBUG"))
LOG_LEVEL = os.getenv("LOG_LEVEL")
RELOAD = bool(os.getenv("AUTO_RELOAD"))

# API setting.
VER_API_ONE = "/api/v1/"
VER_API_TWO = "/api/v2/"

# Auth settings.
OAUTH2_SCHEME = OAuth2PasswordBearer(
    tokenUrl=VER_API_ONE + "auth/login",
    scheme_name="OAuth2CredentialsRequestForm",
    description="Description Description",
)
TOKEN_TYPE = "Bearer"
PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRATION = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS"))

# Session settings.
SESSION_SETTINGS = {
    "autocommit": False,
    "autoflush": False,
    "expire_on_commit": False,
}

# Database settings.
DATABASE_URL = os.getenv("DB_URL")
ECHO = True if os.getenv("DB_ECHO") == "True" else False


SETTINGS_DB = {
    "url": DATABASE_URL,
    "echo": ECHO,
}
