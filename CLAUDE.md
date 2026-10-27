# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Status

- Early-stage scaffold made with `uv init`. No real RAG logic yet.
- `README.md` is empty. No linter or formatter is configured.
- The document endpoints are dummy (static data, no database). Real logic comes later.
- `POST /documents` takes a markdown file upload (`.md` or `.markdown`, UTF-8, max `RAG_MAX_UPLOAD_BYTES`, default 5 MB). The file is read and returned, but not stored yet.

## Testing

- No tests for now. Do not write or update tests unless the user asks.
- `test_create` and `test_create_validation` in `tests/test_documents.py` are outdated (they send JSON, but the route now takes a file) and will fail.

## Project Standards

- This is a RAG (retrieval-augmented generation) project.
- It is production grade. Everything you create must be production grade.
- This applies to all code, including:
  - FastAPI apps and endpoints
  - Database connections
  - Any other component

## Planned Technologies

- This project will use LangChain, LangGraph, PostgreSQL and pgvector.
- None of these are installed yet.
- The user is learning while building. Use these technologies when designing features, and guide them with short, simple explanations.

## Stack

- Python 3.14 (pinned in `.python-version`, `requires-python >=3.14`).
- Package manager: `uv`. Build backend: `uv_build` (src layout).
- Dependencies: `fastapi`, `uvicorn`, `pydantic-settings`, `python-multipart` (needed for file uploads). Dev: `pytest`, `httpx`.
- Local virtualenv lives in `.venv/`.

## Commands

- Install/sync deps: `uv sync`
- Add a dependency: `uv add <package>`
- Run the API: `uv run enterprise-rag` (starts uvicorn via `enterprise_rag:main`)
- Run all tests: `uv run pytest` (tests are on hold, see Testing)
- Run one test: `uv run pytest tests/test_documents.py::test_create`
- Docs UI: `http://localhost:8000/docs` (only when `RAG_ENVIRONMENT` is `local` or `dev`)

## Layout

- `src/` layout: the package is only importable after `uv sync`.
- `app.py`: `create_app()` factory. Wires logging, the global 500 handler and routers.
- `core/`: `config.py` (settings from `RAG_*` env vars or `.env`) and `logging.py`.
- `api/health.py`: `/health` liveness probe.
- `api/v1/`: versioned routers, mounted under `/api/v1`. Add new routers in `api/v1/router.py`.
- `schemas/`: Pydantic request and response models.
- `services/`: business logic, injected into routes with `Depends`. This is where real storage and retrieval will replace the dummy code.
  - `markdown_upload_service.py`: checks and reads the uploaded markdown file.
- `tests/`: pytest tests using FastAPI `TestClient`. On hold for now.
