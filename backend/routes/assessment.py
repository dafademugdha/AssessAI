from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.database.dependencies import get_db
from backend.models.enrollment import Enrollment
from backend.crud.assessment import create_assessment, get_assessment_by_id, get_course_assessments, delete_assessment, publish_assessment
from backend.schemas.assessment import (
    AssessmentCreate,
    AssessmentResponse
)
from backend.models.course import Course
from backend.models.attempt import Attempt
from backend.models.assessment import Assessment
from backend.crud.attempt import (
    get_attempt,
    create_attempt,
)
from backend.schemas.attempt import AttemptResponse
from backend.models.question import Question

from backend.schemas.question import (
    StudentQuestionListResponse,
)

router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"]
)


@router.post(
    "",
    response_model=AssessmentResponse,
    status_code=201
)
@router.post(
    "",
    response_model=AssessmentResponse,
    status_code=201
)
def create_new_assessment(
    data: AssessmentCreate,
    db: Session = Depends(get_db),
):
    # 1. Check whether course exists
    course = (
        db.query(Course)
        .filter(Course.id == data.course_id)
        .first()
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found.",
        )

    # 2. Check whether instructor owns the course
    if course.instructor_id != data.created_by:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to create an assessment for this course.",
        )

    # 3. Create assessment
    assessment = create_assessment(
        db=db,
        course_id=data.course_id,
        created_by=data.created_by,
        title=data.title,
        description=data.description,
        difficulty=data.difficulty,
        duration_minutes=data.duration_minutes,
        mcq_count=data.mcq_count,
        true_false_count=data.true_false_count,
    )

    return assessment


@router.get(
    "/courses/{course_id}/assessments",
    response_model=list[AssessmentResponse]
)
def list_course_assessments(
    course_id: int,
    instructor_id: int,
    db: Session = Depends(get_db),
):
    course = (
        db.query(Course)
        .filter(Course.id == course_id)
        .first()
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found."
        )

    if course.instructor_id != instructor_id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to view assessments for this course."
        )

    return get_course_assessments(
        db=db,
        course_id=course_id
    )


@router.get(
    "/{assessment_id}/questions/student",
    response_model=StudentQuestionListResponse,
)
def get_student_questions(
    assessment_id: int,
    student_id: int,
    db: Session = Depends(get_db),
):
    # 1. Check assessment exists
    assessment = (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id)
        .first()
    )

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found.",
        )

    # 2. Only published assessments can be viewed by students
    if assessment.status != "PUBLISHED":
        raise HTTPException(
            status_code=400,
            detail="Assessment is not published.",
        )

    # 3. Check whether the student is enrolled in the course
    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.course_id == assessment.course_id,
            Enrollment.student_id == student_id,
        )
        .first()
    )

    if enrollment is None:
        raise HTTPException(
            status_code=403,
            detail="Student is not enrolled in this course.",
        )

    # 4. Check whether the student has started this assessment
    attempt = (
        db.query(Attempt)
        .filter(
            Attempt.assessment_id == assessment_id,
            Attempt.student_id == student_id,
            Attempt.status == "IN_PROGRESS",
        )
        .first()
    )

    if attempt is None:
        raise HTTPException(
            status_code=403,
            detail="Student must start the assessment before viewing questions.",
        )

    # 5. Get questions
    questions = (
        db.query(Question)
        .filter(Question.assessment_id == assessment_id)
        .order_by(Question.order_number)
        .all()
    )

    if not questions:
        raise HTTPException(
            status_code=404,
            detail="No questions found for this assessment.",
        )

    return {
        "questions": questions
    }

    

@router.get(
    "/{assessment_id}",
    response_model=AssessmentResponse
)
def get_assessment(
    assessment_id: int,
    instructor_id: int,
    db: Session = Depends(get_db),
):
    assessment = get_assessment_by_id(
        db=db,
        assessment_id=assessment_id
    )

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found."
        )

    if assessment.created_by != instructor_id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to view this assessment."
        )

    return assessment


@router.delete(
    "/{assessment_id}",
    status_code=204
)
def delete_assessment_endpoint(
    assessment_id: int,
    instructor_id: int,
    db: Session = Depends(get_db),
):
    assessment = get_assessment_by_id(
        db=db,
        assessment_id=assessment_id,
    )

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found.",
        )

    if assessment.created_by != instructor_id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to delete this assessment.",
        )

    delete_assessment(
        db=db,
        assessment_id=assessment_id,
    )

    return None


@router.post(
    "/{assessment_id}/publish",
    response_model=AssessmentResponse,
)
def publish_assessment_endpoint(
    assessment_id: int,
    instructor_id: int,
    db: Session = Depends(get_db),
):
    assessment = get_assessment_by_id(
        db=db,
        assessment_id=assessment_id,
    )

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found.",
        )

    if assessment.created_by != instructor_id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to publish this assessment.",
        )

    if assessment.status != "DRAFT":
        raise HTTPException(
            status_code=400,
            detail="Only draft assessments can be published.",
        )

    try:
        published_assessment = publish_assessment(
            db=db,
            assessment=assessment,
        )

        return published_assessment

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

        
@router.post(
    "/{assessment_id}/start",
    response_model=AttemptResponse,
)
def start_assessment(
    assessment_id: int,
    student_id: int,
    db: Session = Depends(get_db),
):
    # 1. Check assessment exists
    assessment = (
        db.query(Assessment)
        .filter(
            Assessment.id == assessment_id
        )
        .first()
    )

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found.",
        )

    # 2. Only published assessments can be started
    if assessment.status != "PUBLISHED":
        raise HTTPException(
            status_code=400,
            detail="Assessment is not published.",
        )
        
    student = (
    db.query(User)
    .filter(User.id == student_id)
    .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found.",
    )

    if student.role != "STUDENT":
        raise HTTPException(
            status_code=403,
            detail="Only students can start an assessment.",
    )

    # 3. Check whether the student is enrolled in the course
    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.course_id == assessment.course_id,
            Enrollment.student_id == student_id,
        )
        .first()
    )

    if enrollment is None:
        raise HTTPException(
            status_code=403,
            detail="Student is not enrolled in this course.",
        )

    # 4. Check whether student already attempted the assessment
    existing_attempt = get_attempt(
        db=db,
        assessment_id=assessment_id,
        student_id=student_id,
    )

    if existing_attempt is not None:
        raise HTTPException(
            status_code=400,
            detail="Student has already attempted this assessment.",
        )

    # 5. Create attempt
    try:
        attempt = create_attempt(
            db=db,
            assessment_id=assessment_id,
            student_id=student_id,
        )

        return attempt

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to start assessment.",
        )
