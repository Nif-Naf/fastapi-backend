import uvicorn
from fastapi import FastAPI

from fastapi_backend.utils.lifespan import lifespan
from settings import DEBUG, HOST, LOG_LEVEL, PORT, RELOAD

# Create instance FastAPI.
app = FastAPI(
    debug=DEBUG,
    lifespan=lifespan,
)


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
