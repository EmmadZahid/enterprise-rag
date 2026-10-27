from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    content: str
    created_at: datetime

class DocumentList(BaseModel):
    items: list[DocumentRead]
    total: int
