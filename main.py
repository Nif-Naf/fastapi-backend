import uvicorn
from fastapi import FastAPI

from fastapi_backend.backend.routers.auth import auth_router
from fastapi_backend.backend.routers.email import email_router
from fastapi_backend.backend.routers.user import user_router
from fastapi_backend.core.settings import DEBUG, HOST, LOG_LEVEL, PORT, RELOAD
from fastapi_backend.core.utils.lifespan import lifespan

# Create instance FastAPI.
app = FastAPI(
    debug=DEBUG,
    lifespan=lifespan,
)
app.include_router(auth_router)
app.include_router(email_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(
        app="__main__:app",
        host=HOST,
        port=PORT,
        log_level=LOG_LEVEL,
        reload=RELOAD,
    )
