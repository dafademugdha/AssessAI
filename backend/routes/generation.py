from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.dependencies import get_db
from backend.models.question import Question
from backend.services.ai.generation_service import (
    generate_assessment_questions,
)
from backend.schemas.question import QuestionResponse


router = APIRouter(
    prefix="/assessments",
    tags=["Assessment Generation"]
)


@router.post(
    "/{assessment_id}/generate",
    response_model=list[QuestionResponse],
)
def generate_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
):
    try:
        # Generate and save questions
        generate_assessment_questions(
            db=db,
            assessment_id=assessment_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
        status_code=500,
        detail=str(e),
    )

    # Fetch the saved questions
    questions = (
        db.query(Question)
        .filter(
            Question.assessment_id == assessment_id
        )
        .order_by(Question.order_number)
        .all()
    )

    return questions