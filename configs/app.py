import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination.utils import disable_installed_extensions_check

from configs.router import api_router
from configs.settings import settings
from dependencies.exception import exception_middleware


@asynccontextmanager
async def register_init(app: FastAPI):
    # await create_table()

    # avoid warnings from fastapi_pagination
    disable_installed_extensions_check()

    if not os.path.exists("logs"):
        os.makedirs("logs")
    # all code before the yield will be executed before the application starts
    yield
    # all code after the yield will be executed after the application stops


def get_application():
    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.PROJECT_VERSION,
        lifespan=register_init,
    )

    register_middleware(application)

    application.include_router(api_router, prefix=settings.URL_PREFIX)

    return application


def register_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_CORS.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.middleware("http")(exception_middleware)
