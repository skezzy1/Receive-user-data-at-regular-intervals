from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from api_router import api_router


BASE_DIR = Path(__file__).resolve().parent.parent

API_V1_PREFIX = "/api/v1"


def get_application() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield

    application = FastAPI(lifespan=lifespan)


    application.include_router(api_router, prefix=API_V1_PREFIX)
    add_pagination(application)

    return application


app = get_application()
