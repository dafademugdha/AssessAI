from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.dependencies import get_db
from backend.models.user import User
from backend.crud.course import (
    create_course,
    get_course_by_id,
    get_courses_by_instructor,
)
from backend.schemas.course import (
    CourseCreate,
    CourseResponse,
)


router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)


@router.post(
    "",
    response_model=CourseResponse,
    status_code=201,
)
def create_new_course(
    data: CourseCreate,
    db: Session = Depends(get_db),
):
    instructor = (
        db.query(User)
        .filter(User.id == data.instructor_id)
        .first()
    )

    if instructor is None:
        raise HTTPException(
            status_code=404,
            detail="Instructor not found.",
        )

    if instructor.role != "INSTRUCTOR":
        raise HTTPException(
            status_code=403,
            detail="Only instructors can create courses.",
        )

    course = create_course(
        db=db,
        title=data.title,
        description=data.description,
        instructor_id=data.instructor_id,
    )

    return course


@router.get(
    "/instructor/{instructor_id}",
    response_model=list[CourseResponse],
)
def list_instructor_courses(
    instructor_id: int,
    db: Session = Depends(get_db),
):
    instructor = (
        db.query(User)
        .filter(User.id == instructor_id)
        .first()
    )

    if instructor is None:
        raise HTTPException(
            status_code=404,
            detail="Instructor not found.",
        )

    if instructor.role != "INSTRUCTOR":
        raise HTTPException(
            status_code=403,
            detail="User is not an instructor.",
        )

    return get_courses_by_instructor(
        db=db,
        instructor_id=instructor_id,
    )


@router.get(
    "/{course_id}",
    response_model=CourseResponse,
)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
):
    course = get_course_by_id(
        db=db,
        course_id=course_id,
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found.",
        )

    return course