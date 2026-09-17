import json
import re

from sqlalchemy.orm import Session
from backend.crud.ai_generation import create_ai_generation

from backend.models.question import Question

from backend.services.ai.assessment_processor import (
    process_assessment_content,
)

from backend.services.ai.regeneration_prompt_builder import (
    build_question_regeneration_prompt,
)

from backend.services.ai.llm_service import (
    generate_with_llm,
)

from backend.schemas.question import (
    GeneratedQuestionResponse,
)

from backend.crud.question import (
    get_questions_by_assessment,
    update_question,
)


def regenerate_question(
    db: Session,
    question_id: int,
) -> GeneratedQuestionResponse:
    """
    Regenerate one question while keeping its ID,
    order number, question type, and assessment.
    """

    # 1. Fetch the question
    question = (
        db.query(Question)
        .filter(Question.id == question_id)
        .first()
    )

    if question is None:
        raise ValueError(
            f"Question with id {question_id} not found."
        )

    # 2. Get the assessment ID
    assessment_id = question.assessment_id

    # 3. Get all existing questions
    existing_questions = get_questions_by_assessment(
        db=db,
        assessment_id=assessment_id,
    )

    # 4. Exclude the question being regenerated
    existing_question_texts = [
        existing.question_text
        for existing in existing_questions
        if existing.id != question_id
    ]

    # 5. Process assessment content
    chunks = process_assessment_content(
        db=db,
        assessment_id=assessment_id,
    )

    if not chunks:
        raise ValueError(
            "No content found for this assessment."
        )

    # 6. Build regeneration prompt
    prompt = build_question_regeneration_prompt(
        chunks=chunks,
        existing_questions=existing_question_texts,
        question_type=question.question_type,
        difficulty=question.difficulty.upper(),
    )

    # 7. Generate with LLM
    response = generate_with_llm(prompt)
    print("\n========== LLM REGENERATION RESPONSE ==========")
    print(response)
    print("===============================================\n")

    # 8. Parse JSON
    try:
        json_match = re.search(
        r"```json\s*(.*?)\s*```",
        response,
        re.DOTALL | re.IGNORECASE,
        )

        if json_match:
            json_text = json_match.group(1)
        else:
            json_text = response.strip()

        data = json.loads(json_text)

    except json.JSONDecodeError:
        raise ValueError(
            "LLM returned invalid JSON."
        )

    # 9. Validate generated question
    validated_response = (
        GeneratedQuestionResponse
        .model_validate(data)
    )

    # 10. Make sure exactly ONE question was generated
    if len(validated_response.questions) != 1:
        raise ValueError(
            "LLM must generate exactly one question."
        )

    new_question = validated_response.questions[0]

    # 11. Make sure the LLM didn't change the question type
    if new_question.question_type != question.question_type:
        raise ValueError(
            "Regenerated question type does not match "
            "the original question type."
        )

    # 12. Make sure difficulty remains the same
    if new_question.difficulty != question.difficulty:
        raise ValueError(
            "Regenerated question difficulty does not match "
            "the original question difficulty."
        )
        
    #create a record in ai_generations
    create_ai_generation(
        db=db,
        assessment_id=question.assessment_id,
        model_name="groq/compound",
        prompt=prompt,
        generation_type="REGENERATION",
        status="SUCCESS",
    )

    # 13. Replace the question in-place
    try:
        update_question(
            db=db,
            question=question,
            question_data=new_question,
        )

        db.commit()

    except Exception:
        db.rollback()
        raise

    return validated_response