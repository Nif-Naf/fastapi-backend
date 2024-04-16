import os
from distutils.util import strtobool

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pika.credentials import PlainCredentials

# Check requirements .env file.
env_conf = load_dotenv()
if not env_conf:
    raise FileNotFoundError("File .env not found.")

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
TOKEN_TYPE = "Bearer"  # noqa
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
# Main DB - Postgres.
SBD = "postgresql+asyncpg"
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_DB")
echo = bool(strtobool(os.getenv("DB_ECHO")))

SETTINGS_DB = {
    "url": f"{SBD}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    "echo": echo,
    "pool_size": 10,
    "max_overflow": 10,
}

# Queue settings.
QUEUE_HOST = os.getenv("QUEUE_HOST")
QUEUE_PORT = int(os.getenv("QUEUE_PORT"))
QUEUE_CONNECTION_PARAMS = {
    "host": QUEUE_HOST,
    "port": QUEUE_PORT,
    "credentials": PlainCredentials(username="guest", password="guest"),
}
# PlainCredentials
