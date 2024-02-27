import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from logger_config import LogConfig

# Check requirements .env file.
env_conf = load_dotenv()
if not env_conf:
    raise FileNotFoundError("File .env not found.")

# Initialization all variables.
HOST = os.getenv("FA_HOST")
PORT = int(os.getenv("FA_PORT"))
DEBUG = bool(os.getenv("FA_DEBUG"))
LOG_LEVEL = os.getenv("FA_LOG_LEVEL")
RELOAD = bool(os.getenv("FA_AUTO_RELOAD"))

# Create instance FastAPI.
app = FastAPI(debug=DEBUG)


@app.get(path="/")
def health_checker():
    return "hello world"


if __name__ == "__main__":
    uvicorn.run(
        app="__main__:app",
        host=HOST,
        port=PORT,
        log_level=LOG_LEVEL,
        reload=RELOAD,
    )
    LogConfig.init_logging_conf()
