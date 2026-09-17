from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.dependencies import get_db

from backend.crud.assessment import get_assessment_by_id
from backend.crud.content import get_content_by_id

from backend.crud.assessment_content import (
    add_content_to_assessment,
    get_assessment_content,
    get_assessment_content_link,
    remove_content_from_assessment,
)

from backend.schemas.content import ContentResponse


router = APIRouter(
    prefix="/assessments",
    tags=["Assessment Content"]
)


# ADD CONTENT TO ASSESSMENT
@router.post(
    "/{assessment_id}/content/{content_id}",
    status_code=201
)
def add_content(
    assessment_id: int,
    content_id: int,
    db: Session = Depends(get_db),
):
    # Check assessment exists
    assessment = get_assessment_by_id(
        db=db,
        assessment_id=assessment_id
    )

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found."
        )

    # Check content exists
    content = get_content_by_id(
        db=db,
        content_id=content_id
    )

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Content not found."
        )

    # Make sure content belongs to the same course
    if content.course_id != assessment.course_id:
        raise HTTPException(
            status_code=400,
            detail="Content does not belong to the assessment's course."
        )

    # Check if already linked
    existing = get_assessment_content_link(
        db=db,
        assessment_id=assessment_id,
        content_id=content_id,
    )

    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail="Content is already added to this assessment."
        )

    return add_content_to_assessment(
        db=db,
        assessment_id=assessment_id,
        content_id=content_id,
    )


# GET SELECTED CONTENT
@router.get(
    "/{assessment_id}/content",
    response_model=list[ContentResponse]
)
def list_assessment_content(
    assessment_id: int,
    db: Session = Depends(get_db),
):
    # Check assessment exists
    assessment = get_assessment_by_id(
        db=db,
        assessment_id=assessment_id
    )

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found."
        )

    return get_assessment_content(
        db=db,
        assessment_id=assessment_id,
    )


# REMOVE CONTENT FROM ASSESSMENT
@router.delete(
    "/{assessment_id}/content/{content_id}",
    status_code=204
)
def remove_content(
    assessment_id: int,
    content_id: int,
    db: Session = Depends(get_db),
):
    # Check assessment exists
    assessment = get_assessment_by_id(
        db=db,
        assessment_id=assessment_id
    )

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found."
        )

    removed = remove_content_from_assessment(
        db=db,
        assessment_id=assessment_id,
        content_id=content_id,
    )

    if removed is None:
        raise HTTPException(
            status_code=404,
            detail="Content is not linked to this assessment."
        )

    return None