from sqlalchemy.orm import Session

from backend.models.content import Content
from backend.models.assessment_content import AssessmentContent

def create_content(
    db: Session,
    course_id: int,
    title: str,
    content_type: str,
    uploaded_by: int,
    source_url: str | None = None,
    file_path: str | None = None,
):
    content = Content(
        course_id=course_id,
        title=title,
        content_type=content_type,
        source_url=source_url,
        file_path=file_path,
        uploaded_by=uploaded_by,
    )

    db.add(content)
    db.commit()
    db.refresh(content)

    return content

def get_course_content(
    db: Session,
    course_id: int
):
    return (
        db.query(Content)
        .filter(Content.course_id == course_id)
        .order_by(Content.created_at.desc())
        .all()
    )
    
def get_content_by_id(
    db: Session,
    content_id: int
):
    return (
        db.query(Content)
        .filter(Content.id == content_id)
        .first()
    )
    
def delete_content(
    db: Session,
    content_id: int
):
    content = (
        db.query(Content)
        .filter(Content.id == content_id)
        .first()
    )

    if content is None:
        return None

    linked_assessment = (
        db.query(AssessmentContent)
        .filter(
            AssessmentContent.content_id == content_id
        )
        .first()
    )

    if linked_assessment is not None:
        return "IN_USE"

    db.delete(content)
    db.commit()

    return content