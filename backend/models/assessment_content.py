from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.base import Base


class AssessmentContent(Base):
    __tablename__ = "assessment_content"

    assessment_id: Mapped[int] = mapped_column(
        ForeignKey("assessments.id", ondelete="CASCADE"),
        primary_key=True
    )

    content_id: Mapped[int] = mapped_column(
        ForeignKey("content.id"),
        primary_key=True
    )