import uvicorn
from fastapi import FastAPI

from fastapi_backend.routers.auth import authorization_router
from fastapi_backend.utils.lifespan import lifespan
from settings import DEBUG, HOST, LOG_LEVEL, PORT, RELOAD

# Create instance FastAPI.
app = FastAPI(
    debug=DEBUG,
    lifespan=lifespan,
)
app.include_router(authorization_router)

if __name__ == "__main__":
    uvicorn.run(
        app="__main__:app",
        host=HOST,
        port=PORT,
        log_level=LOG_LEVEL,
        reload=RELOAD,
    )
