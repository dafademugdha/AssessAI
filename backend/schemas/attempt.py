from datetime import datetime

from pydantic import BaseModel


class AttemptResponse(BaseModel):
    id: int
    assessment_id: int
    student_id: int
    started_at: datetime
    submitted_at: datetime | None
    score: int | None
    status: str
    
class AnswerSubmit(BaseModel):
    question_id: int
    selected_option_id: int | None = None


class AssessmentSubmit(BaseModel):
    answers: list[AnswerSubmit]
    
class ResultItem(BaseModel):
    question_id: int
    question_text: str
    selected_answer: str | None
    correct_answer: str
    is_correct: bool
    explanation: str | None


class AssessmentResultResponse(BaseModel):
    attempt_id: int
    assessment_id: int
    student_id: int
    score: int
    total_questions: int
    result: list[ResultItem]