from sqlalchemy.orm import Session

from backend.models.course import Course


def create_course(
    db: Session,
    title: str,
    description: str | None,
    instructor_id: int,
):
    course = Course(
        title=title,
        description=description,
        instructor_id=instructor_id,
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    return course


def get_course_by_id(
    db: Session,
    course_id: int,
):
    return (
        db.query(Course)
        .filter(Course.id == course_id)
        .first()
    )


def get_courses_by_instructor(
    db: Session,
    instructor_id: int,
):
    return (
        db.query(Course)
        .filter(Course.instructor_id == instructor_id)
        .order_by(Course.created_at.desc())
        .all()
    )