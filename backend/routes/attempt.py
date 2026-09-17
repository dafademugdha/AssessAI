from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.dependencies import get_db
from backend.schemas.attempt import (
    AttemptResponse,
    AssessmentSubmit,
)
from backend.services.attempt_service import submit_assessment
from backend.crud.attempt import get_attempt_by_id
from backend.schemas.attempt import AssessmentResultResponse
from backend.services.result_service import get_assessment_result


router = APIRouter(
    prefix="/attempts",
    tags=["Attempts"],
)

@router.get(
    "/{attempt_id}",
    response_model=AttemptResponse,
)
def get_attempt(
    attempt_id: int,
    student_id: int,
    db: Session = Depends(get_db),
):
    attempt = get_attempt_by_id(
        db=db,
        attempt_id=attempt_id,
    )

    if attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Attempt not found.",
        )

    if attempt.student_id != student_id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to view this attempt.",
        )

    return attempt

@router.post(
    "/{attempt_id}/submit",
    response_model=AttemptResponse,
)
def submit_assessment_endpoint(
    attempt_id: int,
    submission: AssessmentSubmit,
    db: Session = Depends(get_db),
):
    try:
        attempt = submit_assessment(
            db=db,
            attempt_id=attempt_id,
            answers=submission.answers,
        )

        return attempt

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to submit assessment.",
        )
        
@router.get(
    "/{attempt_id}/result",
    response_model=AssessmentResultResponse,
)
def get_result(
    attempt_id: int,
    student_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_assessment_result(
            db=db,
            attempt_id=attempt_id,
            student_id=student_id,
        )

    except ValueError as e:
        message = str(e)

        if message == "Attempt not found.":
            raise HTTPException(
                status_code=404,
                detail=message,
            )

        if message == "You are not allowed to view this attempt.":
            raise HTTPException(
                status_code=403,
                detail=message,
            )

        raise HTTPException(
            status_code=400,
            detail=message,
        )