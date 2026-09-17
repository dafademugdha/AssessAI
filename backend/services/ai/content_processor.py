from sqlalchemy.orm import Session

from backend.models.content import Content

from backend.services.ai.pdf_service import (
    extract_text_from_pdf
)

from backend.services.ai.youtube_service import (
    extract_text_from_youtube
)

from backend.services.ai.text_cleaner import (
    clean_text
)

from backend.services.ai.text_chunker import (
    chunk_text
)


def process_content(
    db: Session,
    content_id: int,
) -> list[str]:
    """
    Fetch content from the database,
    extract text based on content type,
    clean the text,
    and split it into chunks.
    """

    # Get content from database
    content = (
        db.query(Content)
        .filter(Content.id == content_id)
        .first()
    )

    if content is None:
        raise ValueError(
            f"Content with ID {content_id} not found."
        )

    # Extract text based on content type
    if content.content_type.upper() == "PDF":

        if not content.file_path:
            raise ValueError(
                "PDF content does not have a file path."
            )

        raw_text = extract_text_from_pdf(
            content.file_path
        )

    elif content.content_type.upper() == "YOUTUBE":

        if not content.source_url:
            raise ValueError(
                "YouTube content does not have a source URL."
            )

        raw_text = extract_text_from_youtube(
            content.source_url
        )

    else:
        raise ValueError(
            f"Unsupported content type: {content.content_type}"
        )

    # Clean extracted text
    cleaned_text = clean_text(raw_text)

    # Validate extracted text
    if not cleaned_text:
        raise ValueError(
            "No text could be extracted from the content."
        )

    # Split into chunks
    chunks = chunk_text(cleaned_text)

    return chunks