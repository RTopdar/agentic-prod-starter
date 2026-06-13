from datetime import datetime, UTC
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
