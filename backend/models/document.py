from pydantic import BaseModel, Field
from datetime import datetime, UTC


class Document(BaseModel):

    user_id: str

    document_id: str      # same UUID used in Pinecone

    filename: str

    vector_count: int

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )