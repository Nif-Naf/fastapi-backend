import os

from dotenv import load_dotenv

# Check requirements .env file.
env_conf = load_dotenv()
if not env_conf:
    raise FileNotFoundError("File .env not found.")

# Project settings.
HOST = os.getenv("FA_HOST")
PORT = int(os.getenv("FA_PORT"))
DEBUG = bool(os.getenv("FA_DEBUG"))
LOG_LEVEL = os.getenv("FA_LOG_LEVEL")
RELOAD = bool(os.getenv("FA_AUTO_RELOAD"))

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
