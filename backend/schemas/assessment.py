from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AssessmentCreate(BaseModel):
    course_id: int
    created_by: int
    title: str
    description: str | None = None
    difficulty: str
    duration_minutes: int
    mcq_count: int
    true_false_count: int


class AssessmentResponse(BaseModel):
    id: int
    course_id: int
    created_by: int
    title: str
    description: str | None
    difficulty: str
    duration_minutes: int
    mcq_count: int
    true_false_count: int
    status: str
    created_at: datetime
    published_at: datetime | None

    model_config = ConfigDict(from_attributes=True)