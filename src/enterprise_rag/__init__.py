import uvicorn

from enterprise_rag.core.config import get_settings


def main() -> None:
    settings = get_settings()
    uvicorn.run(
        "enterprise_rag.app:create_app",
        factory=True,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
    )
