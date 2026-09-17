from sqlalchemy.orm import Session

from backend.models.attempt import Attempt
from backend.models.answer import Answer
from backend.models.question import Question


def get_assessment_result(
    db: Session,
    attempt_id: int,
    student_id: int,
):
    # 1. Find attempt
    attempt = (
        db.query(Attempt)
        .filter(Attempt.id == attempt_id)
        .first()
    )

    if attempt is None:
        raise ValueError("Attempt not found.")

    # 2. Verify ownership
    if attempt.student_id != student_id:
        raise ValueError(
            "You are not allowed to view this attempt."
        )

    # 3. Result available only after submission
    if attempt.status != "SUBMITTED":
        raise ValueError(
            "Assessment has not been submitted yet."
        )

    # 4. Get answers + questions in ONE query
    rows = (
        db.query(Answer, Question)
        .join(
            Question,
            Answer.question_id == Question.id,
        )
        .filter(
            Answer.attempt_id == attempt_id,
            Question.assessment_id == attempt.assessment_id,
        )
        .order_by(Question.order_number)
        .all()
    )

    if not rows:
        raise ValueError(
            "No answers found for this attempt."
        )

    result = []

    # 5. Build result from joined rows
    for answer, question in rows:
        result.append(
            {
                "question_id": question.id,
                "question_text": question.question_text,
                "selected_answer": answer.selected_answer,
                "correct_answer": question.correct_answer,
                "is_correct": answer.is_correct,
                "explanation": question.explanation,
            }
        )

    return {
        "attempt_id": attempt.id,
        "assessment_id": attempt.assessment_id,
        "student_id": attempt.student_id,
        "score": attempt.score,
        "total_questions": len(result),
        "result": result,
    }

