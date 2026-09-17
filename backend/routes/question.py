from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.question import Question

from backend.database.dependencies import get_db
from backend.schemas.question import QuestionResponse, QuestionUpdate
from backend.services.ai.regeneration_service import regenerate_question
from backend.crud.question import update_question_manual


router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)


@router.post(
    "/{question_id}/regenerate",
    response_model=QuestionResponse,
)
def regenerate_question_endpoint(
    question_id: int,
    db: Session = Depends(get_db),
):
    try:
        regenerate_question(
            db=db,
            question_id=question_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to regenerate question.",
        )

    # Fetch the updated question
    from backend.models.question import Question

    updated_question = (
        db.query(Question)
        .filter(Question.id == question_id)
        .first()
    )

    if updated_question is None:
        raise HTTPException(
            status_code=404,
            detail="Question not found after regeneration.",
        )

    return updated_question

@router.patch(
    "/{question_id}",
    response_model=QuestionResponse,
)
def update_question_endpoint(
    question_id: int,
    question_data: QuestionUpdate,
    db: Session = Depends(get_db),
):
    question = (
        db.query(Question)
        .filter(Question.id == question_id)
        .first()
    )

    if question is None:
        raise HTTPException(
            status_code=404,
            detail="Question not found.",
        )

    try:
        update_question_manual(
            db=db,
            question=question,
            question_data=question_data,
        )

        db.commit()
        db.refresh(question)

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    return question

@router.get(
    "/{question_id}",
    response_model=QuestionResponse,
)
def get_question_endpoint(
    question_id: int,
    db: Session = Depends(get_db),
):
    question = (
        db.query(Question)
        .filter(Question.id == question_id)
        .first()
    )

    if question is None:
        raise HTTPException(
            status_code=404,
            detail="Question not found.",
        )

    return question