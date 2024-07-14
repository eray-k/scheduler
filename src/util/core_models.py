from datetime import datetime, UTC
from uuid import UUID, uuid4

from pydantic import Field, BaseModel


class SimpleIDModel(BaseModel):
    id: int


class UUIDIDModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)


class TimestampModel(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None
