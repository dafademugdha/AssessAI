from sqlalchemy.orm import Session

from backend.models.assessment_content import AssessmentContent
from backend.models.content import Content


def add_content_to_assessment(
    db: Session,
    assessment_id: int,
    content_id: int,
):
    assessment_content = AssessmentContent(
        assessment_id=assessment_id,
        content_id=content_id,
    )

    db.add(assessment_content)
    db.commit()
    db.refresh(assessment_content)

    return assessment_content


def get_assessment_content(
    db: Session,
    assessment_id: int,
):
    return (
        db.query(Content)
        .join(
            AssessmentContent,
            AssessmentContent.content_id == Content.id
        )
        .filter(
            AssessmentContent.assessment_id == assessment_id
        )
        .order_by(Content.created_at.desc())
        .all()
    )


def get_assessment_content_link(
    db: Session,
    assessment_id: int,
    content_id: int,
):
    return (
        db.query(AssessmentContent)
        .filter(
            AssessmentContent.assessment_id == assessment_id,
            AssessmentContent.content_id == content_id,
        )
        .first()
    )


def remove_content_from_assessment(
    db: Session,
    assessment_id: int,
    content_id: int,
):
    assessment_content = get_assessment_content_link(
        db=db,
        assessment_id=assessment_id,
        content_id=content_id,
    )

    if assessment_content is None:
        return None

    db.delete(assessment_content)
    db.commit()

    return assessment_content