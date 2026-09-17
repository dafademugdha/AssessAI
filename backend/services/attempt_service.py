from datetime import datetime

from sqlalchemy.orm import Session

from backend.models.attempt import Attempt
from backend.models.question import Question
from backend.models.option import Option
from backend.crud.answer import create_answer


def submit_assessment(
    db: Session,
    attempt_id: int,
    answers: list,
):
    # 1. Find the attempt
    attempt = (
        db.query(Attempt)
        .filter(Attempt.id == attempt_id)
        .first()
    )

    if attempt is None:
        raise ValueError("Attempt not found.")

    # 2. Prevent resubmission
    if attempt.status != "IN_PROGRESS":
        raise ValueError("Assessment has already been submitted.")

    # 3. Get all questions belonging to this assessment
    questions = (
        db.query(Question)
        .filter(Question.assessment_id == attempt.assessment_id)
        .order_by(Question.order_number)
        .all()
    )

    if not questions:
        raise ValueError("No questions found for this assessment.")

    # Map question IDs to Question objects
    question_map = {
        question.id: question
        for question in questions
    }

    submitted_question_ids = set()
    score = 0

    try:

        # 4. Process submitted answers
        for answer_data in answers:

            question_id = answer_data.question_id
            selected_option_id = answer_data.selected_option_id

            # Check that question belongs to this assessment
            question = question_map.get(question_id)

            if question is None:
                raise ValueError(
                    f"Question {question_id} does not belong to this assessment."
                )

            # Prevent duplicate answers for the same question
            if question_id in submitted_question_ids:
                raise ValueError(
                    f"Answer submitted more than once for question {question_id}."
                )

            submitted_question_ids.add(question_id)

            # 5. Unanswered question
            if selected_option_id is None:

                create_answer(
                    db=db,
                    attempt_id=attempt.id,
                    question_id=question.id,
                    selected_option_id=None,
                    selected_answer=None,
                    is_correct=False,
                )

                continue

            # 6. Validate selected option
            selected_option = (
                db.query(Option)
                .filter(
                    Option.id == selected_option_id,
                    Option.question_id == question.id,
                )
                .first()
            )

            if selected_option is None:
                raise ValueError(
                    f"Option {selected_option_id} does not belong "
                    f"to question {question.id}."
                )

            # 7. Check correctness
            is_correct = selected_option.is_correct

            if is_correct:
                score += 1

            # 8. Save answer
            create_answer(
                db=db,
                attempt_id=attempt.id,
                question_id=question.id,
                selected_option_id=selected_option.id,
                selected_answer=selected_option.option_text,
                is_correct=is_correct,
            )

        # 9. Create answer records for questions
        #    that were not submitted at all.
        #
        #    These are treated as unanswered/incorrect.
        for question in questions:

            if question.id not in submitted_question_ids:

                create_answer(
                    db=db,
                    attempt_id=attempt.id,
                    question_id=question.id,
                    selected_option_id=None,
                    selected_answer=None,
                    is_correct=False,
                )

        # 10. Mark attempt as submitted
        attempt.score = score
        attempt.submitted_at = datetime.utcnow()
        attempt.status = "SUBMITTED"

        # 11. Save everything in one transaction
        db.commit()
        db.refresh(attempt)

        return attempt

    except Exception:
        db.rollback()
        raise