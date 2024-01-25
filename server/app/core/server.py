from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from app.apis import root_api_router
from app.core.config.app import AppConfig
from app.core.utils import logging_middleware


def init_routers(app_: FastAPI) -> None:
    app_.include_router(root_api_router)


def init_logger(app_: FastAPI) -> None:
    app_.middleware("http")(logging_middleware)


def init_static_files(app_: FastAPI) -> None:
    app_.mount("/storage", StaticFiles(directory="storage"), name="static")


def init_cors(app_: FastAPI) -> None:
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=AppConfig.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    # init app
    app = FastAPI(
        title=AppConfig.APP_NAME,
        description=AppConfig.APP_DESCRIPTION,
        version=AppConfig.APP_VERSION,
        docs_url=None if AppConfig.ENVIRONMENT == "production" else "/docs",
        redoc_url=None,
    )
    init_cors(app_=app)
    init_logger(app_=app)
    init_routers(app_=app)
    init_static_files(app_=app)

    return app


app = create_app()
