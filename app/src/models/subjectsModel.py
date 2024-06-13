from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class ScheduleItem(BaseModel):
    day: str = Field(...)
    start_class: datetime = Field(...)
    end_class: datetime = Field(...)


class Subject(BaseModel):
    students: List[UUID] = Field(default_factory=list)
    name: str = Field(...)
    description: str = Field(...)
    schedule: List[ScheduleItem] = Field(default_factory=list)
    group_id: UUID = Field(...)
    professor_id: UUID = Field(...)
    active: bool = Field(default=True)


class SubjectDB(Subject):
    id: Optional[UUID]
