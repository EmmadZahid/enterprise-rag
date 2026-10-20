import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from enterprise_rag.api import health
from enterprise_rag.api.v1.router import api_router
from enterprise_rag.core.config import get_settings
from enterprise_rag.core.logging import configure_logging

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        # Hide interactive docs outside local/dev environments.
        docs_url="/docs" if settings.environment in {"local", "dev"} else None,
        redoc_url=None,
    )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled error on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error"}
        )

    app.include_router(health.router)
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app
