from sqlalchemy.orm import Session
from datetime import datetime

from backend.models.assessment import Assessment
from backend.models.question import Question


def create_assessment(
    db: Session,
    course_id: int,
    created_by: int,
    title: str,
    description: str | None,
    difficulty: str,
    duration_minutes: int,
    mcq_count: int,
    true_false_count: int,
):
    assessment = Assessment(
        course_id=course_id,
        created_by=created_by,
        title=title,
        description=description,
        difficulty=difficulty,
        duration_minutes=duration_minutes,
        mcq_count=mcq_count,
        true_false_count=true_false_count,
        status="DRAFT",
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment

def get_assessment_by_id(
    db: Session,
    assessment_id: int
):
    return (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id)
        .first()
    )
    
def get_course_assessments(
    db: Session,
    course_id: int
):
    return (
        db.query(Assessment)
        .filter(Assessment.course_id == course_id)
        .order_by(Assessment.created_at.desc())
        .all()
    )
    
def delete_assessment(
    db: Session,
    assessment_id: int
):
    assessment = (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id)
        .first()
    )

    if assessment is None:
        return None

    db.delete(assessment)
    db.commit()

    return assessment

def publish_assessment(
    db: Session,
    assessment: Assessment,
):
    questions = (
        db.query(Question)
        .filter(
            Question.assessment_id == assessment.id
        )
        .all()
    )

    # 1. Check total question count
    expected_total = (
        assessment.mcq_count
        + assessment.true_false_count
    )

    actual_total = len(questions)

    if actual_total != expected_total:
        raise ValueError(
            f"Assessment requires {expected_total} questions "
            f"but currently has {actual_total}."
        )

    # 2. Count MCQs and True/False questions
    mcq_questions = [
        question
        for question in questions
        if question.question_type == "MCQ"
    ]

    true_false_questions = [
        question
        for question in questions
        if question.question_type == "TRUE_FALSE"
    ]

    # 3. Validate MCQ count
    if len(mcq_questions) != assessment.mcq_count:
        raise ValueError(
            f"Assessment requires {assessment.mcq_count} MCQs "
            f"but has {len(mcq_questions)}."
        )

    # 4. Validate True/False count
    if len(true_false_questions) != assessment.true_false_count:
        raise ValueError(
            f"Assessment requires "
            f"{assessment.true_false_count} True/False questions "
            f"but has {len(true_false_questions)}."
        )

    # 5. Validate every question
    for question in questions:

        options = question.options

        # MCQ validation
        if question.question_type == "MCQ":

            if len(options) != 4:
                raise ValueError(
                    f"Question {question.id} must have exactly 4 options."
                )

        # True/False validation
        elif question.question_type == "TRUE_FALSE":

            option_texts = {
                option.option_text.strip().lower()
                for option in options
            }

            if option_texts != {"true", "false"}:
                raise ValueError(
                    f"Question {question.id} must have True and False options."
                )

        else:
            raise ValueError(
                f"Question {question.id} has unsupported "
                f"question type: {question.question_type}"
            )

        # Exactly one correct option
        correct_options = [
            option
            for option in options
            if option.is_correct
        ]

        if len(correct_options) != 1:
            raise ValueError(
                f"Question {question.id} must have exactly "
                f"one correct option."
            )

    # 6. Publish
    assessment.status = "PUBLISHED"
    assessment.published_at = datetime.utcnow()

    db.commit()
    db.refresh(assessment)

    return assessment