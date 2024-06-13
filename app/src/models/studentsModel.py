from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class Student(BaseModel):
    name: str = Field(...)
    subjects: List[UUID] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    activate: bool = Field(default=True)


class StudentDB(Student):
    id: Optional[UUID]
