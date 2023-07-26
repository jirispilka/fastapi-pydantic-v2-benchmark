import uvicorn
from fastapi import FastAPI

from app.api import router


def create_app():
    app = FastAPI(openapi_url="/openapi.json", docs_url="/")
    app.include_router(router)
    return app


if __name__ == "__main__":

    _app = create_app()
    uvicorn.run(_app, host="0.0.0.0")
