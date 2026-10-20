from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from enterprise_rag.schemas.document import DocumentCreate, DocumentList, DocumentRead
from enterprise_rag.services.document_service import (
    DocumentService,
    get_document_service,
)

router = APIRouter(prefix="/documents", tags=["documents"])

ServiceDep = Annotated[DocumentService, Depends(get_document_service)]

_NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "Document not found"}}


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
    summary="Create a document",
)
def create_document(payload: DocumentCreate, service: ServiceDep) -> DocumentRead:
    return service.create_document(payload)


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
