from fastapi import APIRouter

from enterprise_rag.api.v1 import documents

api_router = APIRouter()
api_router.include_router(documents.router)
