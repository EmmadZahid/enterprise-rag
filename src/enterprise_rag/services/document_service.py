"""Dummy document service. Replace the bodies with real storage/retrieval later."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from enterprise_rag.schemas.document import DocumentRead

_DUMMY_ID = UUID("00000000-0000-0000-0000-000000000001")


def _dummy_document() -> DocumentRead:
    return DocumentRead(
        id=_DUMMY_ID,
        title="Sample document",
        content="This is a dummy document.",
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
    )


class DocumentService:
    def list_documents(self) -> list[DocumentRead]:
        return [_dummy_document()]

    def get_document(self, document_id: UUID) -> DocumentRead | None:
        document = _dummy_document()
        return document if document.id == document_id else None

    def create_document(self, title: str, content: str) -> DocumentRead:
        return DocumentRead(
            id=uuid4(),
            title=title,
            content=content,
            created_at=datetime.now(UTC),
        )

    def delete_document(self, document_id: UUID) -> bool:
        return document_id == _DUMMY_ID


def get_document_service() -> DocumentService:
    return DocumentService()
