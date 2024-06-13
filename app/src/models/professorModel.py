from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class Professor(BaseModel):
    name: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    activate: bool = Field(default=True)


class ProfessorDB(Professor):
    id: UUID = Field(...)