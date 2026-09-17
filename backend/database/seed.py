from datetime import datetime

from backend.database.connection import SessionLocal
from backend.models import (
    User,
    Course,
    Enrollment,
    Content,
    Assessment,
    AssessmentContent,
    AIGeneration,
    Question,
    Option,
    Attempt,
    Answer,
)


def seed_database():
    db = SessionLocal()

    try:
        # -------------------------
        # 1. USERS
        # -------------------------

        instructor = User(
            name="Instructor A",
            email="instructor@example.com",
            password_hash="dummy_hash",
            role="INSTRUCTOR",
        )

        student = User(
            name="Student 1",
            email="student@example.com",
            password_hash="dummy_hash",
            role="STUDENT",
        )

        db.add_all([instructor, student])
        db.commit()

        db.refresh(instructor)
        db.refresh(student)

        # -------------------------
        # 2. COURSE
        # -------------------------

        course = Course(
            title="Python Programming",
            description="Python fundamentals",
            instructor_id=instructor.id,
        )

        db.add(course)
        db.commit()
        db.refresh(course)

        # -------------------------
        # 3. ENROLLMENT
        # -------------------------

        enrollment = Enrollment(
            student_id=student.id,
            course_id=course.id,
        )

        db.add(enrollment)

        # -------------------------
        # 4. CONTENT
        # -------------------------

        pdf_content = Content(
            course_id=course.id,
            title="Python Basics Notes",
            content_type="PDF",
            file_path="uploads/python_basics.pdf",
            source_url=None,
            uploaded_by=instructor.id,
        )

        youtube_content = Content(
            course_id=course.id,
            title="Python Functions Video",
            content_type="YOUTUBE",
            source_url="https://www.youtube.com/watch?v=example",
            file_path=None,
            uploaded_by=instructor.id,
        )

        db.add_all([pdf_content, youtube_content])
        db.commit()

        db.refresh(pdf_content)
        db.refresh(youtube_content)

        # -------------------------
        # 5. ASSESSMENT
        # -------------------------

        assessment = Assessment(
            course_id=course.id,
            created_by=instructor.id,
            title="Python Basics Test",
            description="Basic Python assessment",
            difficulty="MEDIUM",
            duration_minutes=20,
            mcq_count=2,
            true_false_count=1,
            status="GENERATED",
        )

        db.add(assessment)
        db.commit()
        db.refresh(assessment)

        # -------------------------
        # 6. ASSESSMENT CONTENT
        # -------------------------

        assessment_content_1 = AssessmentContent(
            assessment_id=assessment.id,
            content_id=pdf_content.id,
        )

        assessment_content_2 = AssessmentContent(
            assessment_id=assessment.id,
            content_id=youtube_content.id,
        )

        db.add_all([
            assessment_content_1,
            assessment_content_2,
        ])

        # -------------------------
        # 7. AI GENERATION
        # -------------------------

        ai_generation = AIGeneration(
            assessment_id=assessment.id,
            model_name="Test-LLM",
            prompt="Generate 2 MCQs and 1 True/False question about Python basics.",
            generation_type="INITIAL",
            status="COMPLETED",
        )

        db.add(ai_generation)

        # -------------------------
        # 8. QUESTIONS
        # -------------------------

        q1 = Question(
            assessment_id=assessment.id,
            question_text="Which keyword is used to define a function in Python?",
            question_type="MCQ",
            difficulty="EASY",
            correct_answer="def",
            explanation="The def keyword is used to define a function.",
            order_number=1,
            created_by_ai=True,
        )

        q2 = Question(
            assessment_id=assessment.id,
            question_text="Which data type stores key-value pairs in Python?",
            question_type="MCQ",
            difficulty="EASY",
            correct_answer="dict",
            explanation="A dictionary stores data as key-value pairs.",
            order_number=2,
            created_by_ai=True,
        )

        q3 = Question(
            assessment_id=assessment.id,
            question_text="Python is a dynamically typed language.",
            question_type="TRUE_FALSE",
            difficulty="EASY",
            correct_answer="TRUE",
            explanation="Python determines variable types at runtime.",
            order_number=3,
            created_by_ai=True,
        )

        db.add_all([q1, q2, q3])
        db.commit()

        db.refresh(q1)
        db.refresh(q2)
        db.refresh(q3)

        # -------------------------
        # 9. OPTIONS
        # -------------------------

        options_q1 = [
            Option(
                question_id=q1.id,
                option_text="function",
                is_correct=False,
            ),
            Option(
                question_id=q1.id,
                option_text="def",
                is_correct=True,
            ),
            Option(
                question_id=q1.id,
                option_text="define",
                is_correct=False,
            ),
            Option(
                question_id=q1.id,
                option_text="func",
                is_correct=False,
            ),
        ]

        options_q2 = [
            Option(
                question_id=q2.id,
                option_text="list",
                is_correct=False,
            ),
            Option(
                question_id=q2.id,
                option_text="tuple",
                is_correct=False,
            ),
            Option(
                question_id=q2.id,
                option_text="dict",
                is_correct=True,
            ),
            Option(
                question_id=q2.id,
                option_text="set",
                is_correct=False,
            ),
        ]

        db.add_all(options_q1 + options_q2)
        db.commit()

        db.refresh(options_q1[1])
        db.refresh(options_q2[2])

        # -------------------------
        # 10. ATTEMPT
        # -------------------------

        attempt = Attempt(
            assessment_id=assessment.id,
            student_id=student.id,
            started_at=datetime.utcnow(),
            submitted_at=datetime.utcnow(),
            score=2,
            status="SUBMITTED",
        )

        db.add(attempt)
        db.commit()
        db.refresh(attempt)

        # -------------------------
        # 11. ANSWERS
        # -------------------------

        answer1 = Answer(
            attempt_id=attempt.id,
            question_id=q1.id,
            selected_option_id=options_q1[1].id,
            selected_answer=None,
            is_correct=True,
        )

        answer2 = Answer(
            attempt_id=attempt.id,
            question_id=q2.id,
            selected_option_id=options_q2[0].id,
            selected_answer=None,
            is_correct=False,
        )

        answer3 = Answer(
            attempt_id=attempt.id,
            question_id=q3.id,
            selected_option_id=None,
            selected_answer="TRUE",
            is_correct=True,
        )

        db.add_all([answer1, answer2, answer3])

        db.commit()

        print("Database seeded successfully!")
        print(f"Instructor ID: {instructor.id}")
        print(f"Student ID: {student.id}")
        print(f"Course ID: {course.id}")
        print(f"Assessment ID: {assessment.id}")
        print(f"Attempt ID: {attempt.id}")

    except Exception as e:
        db.rollback()
        print("Database seeding failed!")
        print(e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()