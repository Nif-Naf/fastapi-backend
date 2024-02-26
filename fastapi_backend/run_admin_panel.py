import uvicorn
from admin_panel.settings import (
    ADMIN_DEBUG,
    ADMIN_HOST,
    ADMIN_LOG_LEVEL,
    ADMIN_PORT,
    ADMIN_RELOAD,
)
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app

# Create instance FastAPI.
app = FastAPI(
    title="FastApi backend admin panel",
    docs_url=None,
    debug=ADMIN_DEBUG,
)
app.mount("/", admin_app)

if __name__ == "__main__":
    uvicorn.run(
        app="__main__:app",
        host=ADMIN_HOST,
        port=ADMIN_PORT,
        log_level=ADMIN_LOG_LEVEL,
        reload=ADMIN_RELOAD,
    )
