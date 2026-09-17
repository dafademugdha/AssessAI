from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.base import Base


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True)

    attempt_id: Mapped[int] = mapped_column(
        ForeignKey("attempts.id", ondelete="CASCADE"),
        nullable=False
    )

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False
    )

    selected_option_id: Mapped[int | None] = mapped_column(
        ForeignKey("options.id"),
        nullable=True
    )

    selected_answer: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True
    )