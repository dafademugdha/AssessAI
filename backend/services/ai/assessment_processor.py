from sqlalchemy.orm import Session

from backend.models.assessment_content import AssessmentContent

from backend.services.ai.content_processor import (
    process_content
)


def process_assessment_content(
    db: Session,
    assessment_id: int,
) -> list[str]:
    """
    Process all content linked to an assessment
    and return combined text chunks.
    """

    # Get all content linked to this assessment
    assessment_contents = (
        db.query(AssessmentContent)
        .filter(
            AssessmentContent.assessment_id == assessment_id
        )
        .all()
    )

    if not assessment_contents:
        raise ValueError(
            f"No content is linked to assessment ID {assessment_id}."
        )

    all_chunks = []

    # Process each content source
    for assessment_content in assessment_contents:

        content_id = assessment_content.content_id

        chunks = process_content(
            db=db,
            content_id=content_id
        )

        all_chunks.extend(chunks)

    return all_chunks