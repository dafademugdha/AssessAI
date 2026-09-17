from sqlalchemy.orm import Session

from backend.models.question import Question
from backend.models.option import Option
from backend.schemas.question import GeneratedQuestion, QuestionUpdate

def create_question(
    db: Session,
    assessment_id: int,
    question_data: GeneratedQuestion,
    order_number: int,
) -> Question:
    """
    Create a question and its associated options.
    """

    question = Question(
        assessment_id=assessment_id,
        question_text=question_data.question_text,
        question_type=question_data.question_type,
        difficulty=question_data.difficulty,
        correct_answer=question_data.correct_answer,
        explanation=question_data.explanation,
        order_number=order_number,
        created_by_ai=True,
    )

    db.add(question)
    db.flush()

    for option_data in question_data.options:
        option = Option(
            question_id=question.id,
            option_text=option_data.option_text,
            is_correct=option_data.is_correct,
        )

        db.add(option)

    return question

def get_questions_by_assessment(
    db: Session,
    assessment_id: int,
):
    """
    Get all questions belonging to an assessment.
    """

    return (
        db.query(Question)
        .filter(Question.assessment_id == assessment_id)
        .order_by(Question.order_number)
        .all()
    )

def update_question(
    db: Session,
    question: Question,
    question_data: GeneratedQuestion,
):
    """
    Replace an existing question's content and options.
    The question ID and order number remain unchanged.
    """

    question.question_text = question_data.question_text
    question.question_type = question_data.question_type
    question.difficulty = question_data.difficulty
    question.correct_answer = question_data.correct_answer
    question.explanation = question_data.explanation
    question.created_by_ai = True

    # Remove old options
    for option in question.options:
        db.delete(option)

    db.flush()

    # Add new options
    for option_data in question_data.options:
        option = Option(
            question_id=question.id,
            option_text=option_data.option_text,
            is_correct=option_data.is_correct,
        )

        db.add(option)

    db.flush()

    return question

def get_questions_by_assessment(
    db: Session,
    assessment_id: int,
):
    """
    Get all questions belonging to an assessment.
    """

    return (
        db.query(Question)
        .filter(Question.assessment_id == assessment_id)
        .order_by(Question.order_number)
        .all()
    )


def update_question(
    db: Session,
    question: Question,
    question_data: GeneratedQuestion,
):
    """
    Replace an existing question's content and options.

    The question ID, assessment ID, and order number
    remain unchanged.
    """

    # Update question fields
    question.question_text = question_data.question_text
    question.question_type = question_data.question_type
    question.difficulty = question_data.difficulty
    question.correct_answer = question_data.correct_answer
    question.explanation = question_data.explanation
    question.created_by_ai = True

    # Delete existing options
    for option in question.options:
        db.delete(option)

    db.flush()

    # Create new options
    for option_data in question_data.options:
        option = Option(
            question_id=question.id,
            option_text=option_data.option_text,
            is_correct=option_data.is_correct,
        )

        db.add(option)

    db.flush()

    return question

def update_question_manual(
    db: Session,
    question: Question,
    question_data: QuestionUpdate,
):
    """
    Manually update a question and optionally replace its options.
    """

    # Update fields that were provided
    question.created_by_ai = False
    if question_data.question_text is not None:
        question.question_text = question_data.question_text

    if question_data.difficulty is not None:
        question.difficulty = question_data.difficulty

    if question_data.explanation is not None:
        question.explanation = question_data.explanation

    # Replace options if provided
    if question_data.options is not None:

        options = question_data.options

        # Validate options based on question type
        correct_options = [
            option
            for option in options
            if option.is_correct
        ]

        if len(correct_options) != 1:
            raise ValueError(
                "Question must have exactly one correct option."
            )

        if question.question_type == "MCQ":

            if len(options) != 4:
                raise ValueError(
                    "MCQ must have exactly 4 options."
                )

        elif question.question_type == "TRUE_FALSE":

            option_texts = {
                option.option_text.strip().lower()
                for option in options
            }

            if option_texts != {"true", "false"}:
                raise ValueError(
                    "TRUE_FALSE question must have True and False options."
                )

        # Delete existing options
        for option in question.options:
            db.delete(option)

        db.flush()

        # Create new options
        for option_data in options:
            option = Option(
                question_id=question.id,
                option_text=option_data.option_text,
                is_correct=option_data.is_correct,
            )

            db.add(option)

    db.flush()

    return question