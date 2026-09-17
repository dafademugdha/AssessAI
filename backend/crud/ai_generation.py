from sqlalchemy.orm import Session

from backend.models.ai_generation import AIGeneration


def create_ai_generation(
    db: Session,
    assessment_id: int,
    model_name: str,
    prompt: str,
    generation_type: str,
    status: str,
):
    generation = AIGeneration(
        assessment_id=assessment_id,
        model_name=model_name,
        prompt=prompt,
        generation_type=generation_type,
        status=status,
    )

    db.add(generation)
    db.flush()

    return generation