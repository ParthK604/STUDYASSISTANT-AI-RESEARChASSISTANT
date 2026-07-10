from pydantic import BaseModel, Field
from datetime import datetime, UTC


class User(BaseModel):
    clerk_id: str
    name: str
    email: str
    provider: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))