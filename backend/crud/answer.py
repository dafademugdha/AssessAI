from sqlalchemy.orm import Session

from backend.models.answer import Answer


def create_answer(
    db: Session,
    attempt_id: int,
    question_id: int,
    selected_option_id: int | None,
    selected_answer: str | None,
    is_correct: bool,
):
    answer = Answer(
        attempt_id=attempt_id,
        question_id=question_id,
        selected_option_id=selected_option_id,
        selected_answer=selected_answer,
        is_correct=is_correct,
    )

    db.add(answer)

    return answer