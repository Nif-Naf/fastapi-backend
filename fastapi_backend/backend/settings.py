import json
import os
import sys
from logging import config

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))

###################
# -- Init loggers.
###################

logger_conf = os.path.join(MAIN_DIR, "../core/configs/logging_config.json")
with open(logger_conf) as f:
    conf = json.load(f)
    conf["handlers"]["warn_handler"]["filename"] = os.path.join(
        MAIN_DIR, "logs/critical.txt"
    )
    conf["handlers"]["auth_handler"]["filename"] = os.path.join(
        MAIN_DIR, "logs/auth.txt"
    )
    config.dictConfig(conf)

###################
# -- Loading and setting variables.
###################

if "pytest" in sys.argv[0]:
    path = os.path.join(MAIN_DIR, "../core/envs/.env.test")
    env_conf = load_dotenv(dotenv_path=path)
    if not env_conf:
        mess = f"File .env.test not found at path: {path}"
        raise Warning(mess)

    DATABASE_URL = os.getenv("DB_URL")
else:
    path = os.path.join(MAIN_DIR, "../core/envs/.env")
    env_conf = load_dotenv(dotenv_path=path)
    if not env_conf:
        raise Warning(f"File .env not found at path: {path}")

    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    DATABASE_URL = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:"
        f"{DB_PORT}/{DB_NAME}"
    )


###################
# -- Project settings.
###################

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
DEBUG = bool(os.getenv("DEBUG"))
LOG_LEVEL = os.getenv("LOG_LEVEL")
RELOAD = bool(os.getenv("AUTO_RELOAD"))

###################
# -- Database settings.
###################
SETTINGS_DB = {
    "url": DATABASE_URL,
    "echo": True if os.getenv("DB_ECHO") == "True" else False,
}
SESSION_SETTINGS = {
    "autocommit": False,
    "autoflush": False,
    "expire_on_commit": False,
}

###################
# -- API setting.
###################
VER_API_ONE = "/api/v1/"
VER_API_TWO = "/api/v2/"

###################
# -- Auth settings.
###################
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
