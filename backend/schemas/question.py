from pydantic import BaseModel, Field, model_validator
from typing import Literal
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class OptionSchema(BaseModel):
    option_text: str
    is_correct: bool


class GeneratedQuestion(BaseModel):
    question_text: str
    question_type: Literal["MCQ", "TRUE_FALSE"]
    difficulty: Literal["EASY", "MEDIUM", "HARD"]

    options: list[OptionSchema]

    correct_answer: str

    explanation: str | None = None

    @model_validator(mode="after")
    def validate_question(self):

        if self.question_type == "MCQ":

            if len(self.options) < 2:
                raise ValueError(
                    "MCQ must have at least 2 options."
                )

            correct_options = [
                option
                for option in self.options
                if option.is_correct
            ]

            if len(correct_options) != 1:
                raise ValueError(
                    "MCQ must have exactly one correct option."
                )

        elif self.question_type == "TRUE_FALSE":

            option_texts = {
                option.option_text.strip().lower()
                for option in self.options
            }

            if option_texts != {"true", "false"}:
                raise ValueError(
                    "TRUE_FALSE question must have True and False options."
                )

            correct_options = [
                option
                for option in self.options
                if option.is_correct
            ]

            if len(correct_options) != 1:
                raise ValueError(
                    "TRUE_FALSE question must have exactly one correct option."
                )

        return self


class GeneratedQuestionResponse(BaseModel):
    questions: list[GeneratedQuestion]
    
class OptionResponse(BaseModel):
    id: int
    option_text: str
    is_correct: bool

    model_config = ConfigDict(from_attributes=True)


class QuestionResponse(BaseModel):
    id: int
    assessment_id: int
    question_text: str
    question_type: str
    difficulty: str
    correct_answer: str
    explanation: str | None
    order_number: int
    created_by_ai: bool
    created_at: datetime
    updated_at: datetime

    options: list[OptionResponse]

    model_config = ConfigDict(from_attributes=True)
    
class QuestionUpdate(BaseModel):
    question_text: str | None = None
    difficulty: Literal["EASY", "MEDIUM", "HARD"] | None = None
    explanation: str | None = None

    options: list[OptionSchema] | None = None
    
class StudentOptionResponse(BaseModel):
    id: int
    option_text: str

    model_config = ConfigDict(from_attributes=True)


class StudentQuestionResponse(BaseModel):
    id: int
    question_text: str
    question_type: str
    difficulty: str
    order_number: int
    options: list[StudentOptionResponse]

    model_config = ConfigDict(from_attributes=True)


class StudentQuestionListResponse(BaseModel):
    questions: list[StudentQuestionResponse]