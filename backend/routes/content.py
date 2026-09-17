from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.database.dependencies import get_db
from backend.schemas.content import ContentResponse, YouTubeContentCreate
from backend.models.course import Course

from backend.crud.content import (
    create_content,
    get_course_content, get_content_by_id, delete_content
)



router = APIRouter(
    prefix="/courses/{course_id}/content",
    tags=["Content"]
)
content_detail_router = APIRouter(
    prefix="/content",
    tags=["Content"]
)


UPLOAD_DIRECTORY = Path("uploads/pdfs")


@router.post(
    "/pdf",
    response_model=ContentResponse,
    status_code=201
)
async def upload_pdf(
    course_id: int,
    title: str = Form(...),
    uploaded_by: int = Form(...),
    file: UploadFile = File(...),
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

    if course.instructor_id != uploaded_by:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to add content to this course."
    )

    # -------------------------
    # Validate PDF
    # -------------------------

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # -------------------------
    # Create uploads directory
    # -------------------------

    UPLOAD_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    # -------------------------
    # Generate unique filename
    # -------------------------

    file_name = f"{uuid4()}_{file.filename}"

    file_path = UPLOAD_DIRECTORY / file_name

    # -------------------------
    # Save file
    # -------------------------

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # -------------------------
    # Save metadata in database
    # -------------------------

    content = create_content(
        db=db,
        course_id=course_id,
        title=title,
        content_type="PDF",
        uploaded_by=uploaded_by,
        file_path=str(file_path),
    )

    return content

@router.post(
    "/youtube",
    response_model=ContentResponse,
    status_code=201
)
def add_youtube_content(
    course_id: int,
    data: YouTubeContentCreate,
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

    if course.instructor_id != data.uploaded_by:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to add content to this course."
    )
    
    if "youtube.com/" not in data.source_url and "youtu.be/" not in data.source_url:
        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube URL."
        )

    content = create_content(
        db=db,
        course_id=course_id,
        title=data.title,
        content_type="YOUTUBE",
        uploaded_by=data.uploaded_by,
        source_url=data.source_url,
        file_path=None,
    )

    return content

@router.get(
    "",
    response_model=list[ContentResponse]
)
def list_course_content(
    course_id: int,
    db: Session = Depends(get_db),
):
    return get_course_content(
        db=db,
        course_id=course_id
    )
    
@content_detail_router.get(
    "/{content_id}",
    response_model=ContentResponse
)
def get_content(
    content_id: int,
    db: Session = Depends(get_db),
):
    content = get_content_by_id(
        db=db,
        content_id=content_id
    )

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Content not found."
        )

    return content

@content_detail_router.delete(
    "/{content_id}",
    status_code=204
)
def delete_content_endpoint(
    content_id: int,
    db: Session = Depends(get_db),
):
    content = delete_content(
        db=db,
        content_id=content_id
    )

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Content not found."
        )
        
    if content == "IN_USE":
        raise HTTPException(
            status_code=409,
            detail="Cannot delete this content because it is being used by an assessment."
        )

    return None