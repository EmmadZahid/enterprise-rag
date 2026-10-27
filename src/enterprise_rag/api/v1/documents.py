from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status

from enterprise_rag.core.config import Settings, get_settings
from enterprise_rag.services.markdown_upload_service import read_markdown_file
from enterprise_rag.schemas.document import DocumentList, DocumentRead
from enterprise_rag.services.document_service import (
    DocumentService,
    get_document_service,
)

router = APIRouter(prefix="/documents", tags=["documents"])

ServiceDep = Annotated[DocumentService, Depends(get_document_service)]
SettingsDep = Annotated[Settings, Depends(get_settings)]

_NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "Document not found"}}
_UPLOAD_ERRORS = {
    status.HTTP_413_CONTENT_TOO_LARGE: {"description": "File is too large"},
    status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {"description": "Only .md files are allowed"},
    status.HTTP_422_UNPROCESSABLE_CONTENT: {"description": "File is empty or not UTF-8 text"},
}

@router.get("", response_model=DocumentList, summary="List documents")
def list_documents(service: ServiceDep) -> DocumentList:
    items = service.list_documents()
    return DocumentList(items=items, total=len(items))


@router.get(
    "/{document_id}",
    response_model=DocumentRead,
    responses=_NOT_FOUND,
    summary="Get a document",
)
def get_document(document_id: UUID, service: ServiceDep) -> DocumentRead:
    document = service.get_document(document_id)
    if document is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")
    return document


@router.post(
    "",
    response_model=DocumentRead,
    status_code=status.HTTP_201_CREATED,
    responses=_UPLOAD_ERRORS,
    summary="Upload a document",
)
async def create_document(file: Annotated[UploadFile, File(description="Markdown file (.md)")], 
                          service: ServiceDep, 
                          settings: SettingsDep) -> DocumentRead:
    title, content = await read_markdown_file(file, settings.max_upload_bytes)
    return service.create_document(title, content)


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=_NOT_FOUND,
    summary="Delete a document",
)
def delete_document(document_id: UUID, service: ServiceDep) -> Response:
    if not service.delete_document(document_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
