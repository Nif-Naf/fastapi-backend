import os

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

# Auth settings.
AUTH_PREFIX = "/api/v1/auth"
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl=AUTH_PREFIX + "/login")
PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")
EXPIRATION = {
    "days": int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", 0)),
    "hours": int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", 1)),
    "minutes": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 0)),
}

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

MAIN_SETTINGS_DB = {
    "url": f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}",
    "echo": bool(os.getenv("DB_ECHO")),
    "pool_size": 10,
    "max_overflow": 10,
}
