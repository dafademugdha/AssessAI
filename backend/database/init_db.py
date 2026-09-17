from backend.database.base import Base
from backend.database.connection import engine

# Import all models so SQLAlchemy registers the tables
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


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()