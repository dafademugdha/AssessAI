from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ContentResponse(BaseModel):
    id: int
    course_id: int
    title: str
    content_type: str
    source_url: str | None
    file_path: str | None
    uploaded_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class YouTubeContentCreate(BaseModel):
    title: str
    source_url: str
    uploaded_by: int