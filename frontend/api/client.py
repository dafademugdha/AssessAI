import requests


BASE_URL = "http://127.0.0.1:8000"


# --------------------------------
# Course APIs
# --------------------------------

def get_instructor_courses(instructor_id: int):
    response = requests.get(
        f"{BASE_URL}/courses/instructor/{instructor_id}"
    )

    response.raise_for_status()
    return response.json()


def create_course(
    title: str,
    description: str,
    instructor_id: int,
):
    response = requests.post(
        f"{BASE_URL}/courses",
        json={
            "title": title,
            "description": description,
            "instructor_id": instructor_id,
        },
    )

    response.raise_for_status()
    return response.json()


def get_course(course_id: int):
    response = requests.get(
        f"{BASE_URL}/courses/{course_id}"
    )

    response.raise_for_status()
    return response.json()


# --------------------------------
# Content APIs
# --------------------------------

def get_course_content(course_id: int):
    response = requests.get(
        f"{BASE_URL}/courses/{course_id}/content"
    )

    response.raise_for_status()
    return response.json()


def upload_pdf(
    course_id: int,
    title: str,
    uploaded_by: int,
    file,
):
    response = requests.post(
        f"{BASE_URL}/courses/{course_id}/content/pdf",
        data={
            "title": title,
            "uploaded_by": uploaded_by,
        },
        files={
            "file": (
                file.name,
                file.getvalue(),
                "application/pdf",
            )
        },
    )

    response.raise_for_status()
    return response.json()


def add_youtube_content(
    course_id: int,
    title: str,
    source_url: str,
    uploaded_by: int,
):
    response = requests.post(
        f"{BASE_URL}/courses/{course_id}/content/youtube",
        json={
            "title": title,
            "source_url": source_url,
            "uploaded_by": uploaded_by,
        },
    )

    response.raise_for_status()
    return response.json()


def delete_content(content_id: int):
    response = requests.delete(
        f"{BASE_URL}/content/{content_id}"
    )

    response.raise_for_status()
    return True

# --------------------------------
# Assessment APIs
# --------------------------------

def create_assessment(
    course_id: int,
    created_by: int,
    title: str,
    description: str,
    difficulty: str,
    duration_minutes: int,
    mcq_count: int,
    true_false_count: int,
):
    response = requests.post(
        f"{BASE_URL}/assessments",
        json={
            "course_id": course_id,
            "created_by": created_by,
            "title": title,
            "description": description,
            "difficulty": difficulty,
            "duration_minutes": duration_minutes,
            "mcq_count": mcq_count,
            "true_false_count": true_false_count,
        },
    )

    response.raise_for_status()
    return response.json()


def get_course_assessments(
    course_id: int,
    instructor_id: int,
):
    response = requests.get(
        f"{BASE_URL}/assessments/courses/{course_id}/assessments",
        params={
            "instructor_id": instructor_id,
        },
    )

    response.raise_for_status()
    return response.json()


def get_assessment(
    assessment_id: int,
    instructor_id: int,
):
    response = requests.get(
        f"{BASE_URL}/assessments/{assessment_id}",
        params={
            "instructor_id": instructor_id,
        },
    )

    response.raise_for_status()
    return response.json()