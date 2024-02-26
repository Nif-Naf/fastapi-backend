import uvicorn
from fastapi import FastAPI

from backend.lifespan import lifespan
from backend.routers.auth import auth_router
from backend.routers.email import email_router
from backend.routers.user import user_router
from backend.settings import DEBUG, HOST, LOG_LEVEL, PORT, RELOAD

# Create instance FastAPI.
app = FastAPI(
    debug=DEBUG,
    title="Authentication",
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
