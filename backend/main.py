from fastapi import FastAPI

from backend.routes.content import (router as content_router, content_detail_router)
from backend.routes.assessment import router as assessment_router
from backend.routes.assessment_content import router as assessment_content_router
from backend.routes.question import router as question_router
from backend.routes.generation import router as generation_router
from backend.routes.attempt import router as attempt_router
from backend.routes.course import router as course_router

app = FastAPI(
    title="LearnHub AI Assessment Generator",
    version="1.0.0"
)

app.include_router(content_detail_router)
app.include_router(content_router)
app.include_router(assessment_router)
app.include_router(assessment_content_router)
app.include_router(question_router)
app.include_router(generation_router)
app.include_router(attempt_router)
app.include_router(course_router)

@app.get("/")
def root():
    return {
        "message": "LearnHub AI Assessment Generator API is running"
    }