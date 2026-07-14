from datetime import datetime, UTC

from pydantic import BaseModel, Field


class Message(BaseModel):
    user_id: str
    role: str
    content: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )