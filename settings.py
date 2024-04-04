import os
from distutils.util import strtobool

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

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
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
name = os.getenv("DB_DB")
echo = bool(strtobool(os.getenv("DB_ECHO")))

MAIN_SETTINGS_DB = {
    "url": f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}",
    "echo": echo,
    "pool_size": 10,
    "max_overflow": 10,
}
