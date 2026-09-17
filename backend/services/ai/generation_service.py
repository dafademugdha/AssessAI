import json

from sqlalchemy.orm import Session
from backend.crud.ai_generation import create_ai_generation

from backend.models.assessment import Assessment
from backend.services.ai.assessment_processor import (
    process_assessment_content,
)
from backend.services.ai.prompt_builder import (
    build_question_generation_prompt,
)
from backend.services.ai.llm_service import (
    generate_with_llm,
)
from backend.schemas.question import (
    GeneratedQuestionResponse
)
from backend.crud.question import (
    create_question,
)
from backend.models.question import Question


def generate_assessment_questions(
    db: Session,
    assessment_id: int,
) -> GeneratedQuestionResponse:
    """
    Generate AI questions for an assessment and save them
    along with their options in the database.
    """

    # -----------------------------------
    # 1. Get assessment
    # -----------------------------------

    assessment = (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id)
        .first()
    )

    if not assessment:
        raise ValueError(
            f"Assessment with id {assessment_id} not found."
        )
        
    existing_questions = (
    db.query(Question)
    .filter(
        Question.assessment_id == assessment_id
    )
    .count()
    )

    if existing_questions > 0:
        raise ValueError(
        "Assessment already has generated questions. "
        "Use question regeneration to replace individual questions."
    )

    # -----------------------------------
    # 2. Process linked content
    # -----------------------------------

    chunks = process_assessment_content(
        db=db,
        assessment_id=assessment_id,
    )

    if not chunks:
        raise ValueError(
            "No content found for this assessment."
        )

    # -----------------------------------
    # 3. Build prompt
    # -----------------------------------

    prompt = build_question_generation_prompt(
        chunks=chunks,
        mcq_count=assessment.mcq_count,
        true_false_count=assessment.true_false_count,
        difficulty=assessment.difficulty.upper(),
    )

    # -----------------------------------
    # 4. Generate response using LLM
    # -----------------------------------

    response = generate_with_llm(prompt)

    # -----------------------------------
    # 5. Record AI generated response
    # -----------------------------------
    
    create_ai_generation(
    db=db,
    assessment_id=assessment_id,
    model_name="groq/compound",
    prompt=prompt,
    generation_type="INITIAL",
    status="SUCCESS",
    )
    
    # -----------------------------------
    # 5. Parse JSON
    # -----------------------------------

    try:
        data = json.loads(response)

    except json.JSONDecodeError:
        raise ValueError(
            "LLM returned invalid JSON."
        )

    # -----------------------------------
    # 6. Validate LLM response
    # -----------------------------------

    validated_response = (
        GeneratedQuestionResponse
        .model_validate(data)
    )

    # -----------------------------------
    # 7. Save questions and options
    # -----------------------------------

    try:

        for order_number, question_data in enumerate(
            validated_response.questions,
            start=1,
        ):

            create_question(
                db=db,
                assessment_id=assessment_id,
                question_data=question_data,
                order_number=order_number,
            )

        # -----------------------------------
        # 8. Commit everything once
        # -----------------------------------

        db.commit()

    except Exception:

        db.rollback()
        raise

    return validated_response
