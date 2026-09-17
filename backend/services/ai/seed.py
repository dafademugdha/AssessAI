# from backend.services.ai.pdf_service import extract_text_from_pdf

# text = extract_text_from_pdf(
#     "uploads\\pdfs\\41b61a98-2ec5-421d-817b-9ec3d9e6846d_OS_Full_Notes.pdf"
# )

# print(text[:2000])

# from backend.services.ai.youtube_service import (
#     extract_text_from_youtube
# )


# url = "https://youtu.be/3XCVM3G3pns?si=jLdhKWnGSud6I98U"

# text = extract_text_from_youtube(url)

# print(text[:2000])

# from backend.services.ai.text_cleaner import clean_text
# sample_text =text


# cleaned_text = clean_text(sample_text)

# print(cleaned_text)

# from backend.services.ai.text_cleaner import clean_text
# from backend.services.ai.text_chunker import chunk_text

# chunks = chunk_text(
#     cleaned_text,
#     chunk_size=500,
#     chunk_overlap=40
# )

# for i, chunk in enumerate(chunks):
#     print(f"\n--- Chunk {i + 1} ---")
#     print(chunk)
    
# from backend.database.connection import SessionLocal
# from backend.services.ai.content_processor import (
#     process_content
# )
# db = SessionLocal()
# try:
#     chunks = process_content(
#         db=db,
#         content_id=4
#     )
#     print(f"Total chunks: {len(chunks)}")
#     for i, chunk in enumerate(chunks[:3]):
#         print(f"\n--- Chunk {i + 1} ---")
#         print(chunk[:500])
# finally:
#     db.close()

from backend.database.connection import SessionLocal

from backend.services.ai.assessment_processor import (
    process_assessment_content
)


db = SessionLocal()

try:
    chunks = process_assessment_content(
        db=db,
        assessment_id=4
    )

    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks[:5]):
        print(f"\n--- Chunk {i + 1} ---")
        print(chunk[:500])

finally:
    db.close()