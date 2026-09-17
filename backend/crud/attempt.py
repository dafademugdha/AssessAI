from sqlalchemy.orm import Session

from backend.models.attempt import Attempt


def get_attempt(
    db: Session,
    assessment_id: int,
    student_id: int,
):
    return (
        db.query(Attempt)
        .filter(
            Attempt.assessment_id == assessment_id,
            Attempt.student_id == student_id,
        )
        .first()
    )


def create_attempt(
    db: Session,
    assessment_id: int,
    student_id: int,
):
    attempt = Attempt(
        assessment_id=assessment_id,
        student_id=student_id,
        status="IN_PROGRESS",
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt

def get_attempt_by_id(
    db: Session,
    attempt_id: int,
):
    return (
        db.query(Attempt)
        .filter(Attempt.id == attempt_id)
        .first()
    )