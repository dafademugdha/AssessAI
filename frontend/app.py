import streamlit as st

from api.client import (
    get_instructor_courses,
    get_course_content,
    upload_pdf,
    add_youtube_content,
    delete_content,
    create_assessment,
    get_course_assessments,
    get_assessment,
)


st.set_page_config(
    page_title="AssessAI",
    page_icon="📝",
    layout="wide",
)


# -----------------------------
# App Header
# -----------------------------

st.title("📝 AssessAI")
st.caption("AI-Powered Assessment Generation Platform")


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("Navigation")

role = st.sidebar.selectbox(
    "Select Role",
    ["Instructor", "Student"],
)


if role == "Instructor":

    st.sidebar.subheader("Instructor")

    page = st.sidebar.radio(
        "Go to",
        [
            "Dashboard",
            "Content",
            "Assessments",
        ],
    )

else:

    st.sidebar.subheader("Student")

    page = st.sidebar.radio(
        "Go to",
        [
            "Dashboard",
            "My Assessments",
        ],
    )
    
# -----------------------------
# Session State
# -----------------------------

if "instructor_id" not in st.session_state:
    st.session_state.instructor_id = None

if "selected_course_id" not in st.session_state:
    st.session_state.selected_course_id = None

if "selected_course_title" not in st.session_state:
    st.session_state.selected_course_title = None


# -----------------------------
# Instructor Pages
# -----------------------------

if role == "Instructor":

    if page == "Dashboard":

        st.header("Instructor Dashboard")

        instructor_id = st.number_input(
            "Instructor ID",
            min_value=1,
            value=4,
            step=1,
        )
        st.session_state.instructor_id = instructor_id

        st.divider()

        try:

            courses = get_instructor_courses(
                instructor_id
            )

            st.subheader("Your Courses")

            if not courses:

                st.info(
                    "You don't have any courses yet."
                )

            else:

                cols = st.columns(3)

                for index, course in enumerate(courses):

                    with cols[index % 3]:

                        st.markdown(
                            f"### 📚 {course['title']}"
                        )

                        if course["description"]:
                            st.write(
                                course["description"]
                            )

                        st.caption(
                            f"Course ID: {course['id']}"
                        )

                        if st.button(
                            "Open Course",
                            key=f"course_{course['id']}",
                        ):
                            st.session_state.selected_course_id = course["id"]
                            st.session_state.selected_course_title = course["title"]
                            st.rerun()

        except Exception as e:

            st.error(
                f"Unable to load courses: {e}"
            )
            
    elif page == "Content":

        course_id = st.session_state.get(
            "selected_course_id"
        )

        course_title = st.session_state.get(
            "selected_course_title"
        )

        instructor_id = st.session_state.get("instructor_id")

        if course_id is None:

            st.warning(
                "Please open a course from the Dashboard first."
            )

        else:

            st.header(f"📚 {course_title}")

            st.subheader("Course Content")

            # --------------------------------
            # Load existing content
            # --------------------------------

            try:

                contents = get_course_content(course_id)

            except Exception as e:

                st.error(
                    f"Unable to load course content: {e}"
                )

                contents = []

            # --------------------------------
            # Add Content
            # --------------------------------

            st.divider()

            st.subheader("Add Content")

            content_type = st.radio(
                "Select content type",
                ["PDF", "YouTube"],
                horizontal=True,
            )

            # --------------------------------
            # PDF Upload
            # --------------------------------

            if content_type == "PDF":

                title = st.text_input(
                    "Content Title"
                )

                uploaded_file = st.file_uploader(
                    "Upload PDF",
                    type=["pdf"],
                )

                if st.button(
                    "Upload PDF",
                    type="primary",
                ):

                    if not title:
                        st.warning(
                            "Please enter a title."
                        )

                    elif uploaded_file is None:
                        st.warning(
                            "Please select a PDF."
                        )

                    else:

                        try:

                            upload_pdf(
                                course_id=course_id,
                                title=title,
                                uploaded_by=instructor_id,
                                file=uploaded_file,
                            )

                            st.success(
                                "PDF uploaded successfully!"
                            )

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Failed to upload PDF: {e}"
                            )

            # --------------------------------
            # YouTube
            # --------------------------------

            else:

                title = st.text_input(
                    "Content Title"
                )

                youtube_url = st.text_input(
                    "YouTube URL"
                )

                if st.button(
                    "Add YouTube Video",
                    type="primary",
                ):

                    if not title:
                        st.warning(
                            "Please enter a title."
                        )

                    elif not youtube_url:
                        st.warning(
                            "Please enter a YouTube URL."
                        )

                    else:

                        try:

                            add_youtube_content(
                                course_id=course_id,
                                title=title,
                                source_url=youtube_url,
                                uploaded_by=instructor_id,
                            )

                            st.success(
                                "YouTube video added successfully!"
                            )

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Failed to add YouTube video: {e}"
                            )

            # --------------------------------
            # Existing Content
            # --------------------------------

            st.divider()

            st.subheader("Existing Content")

            if not contents:

                st.info(
                    "No content has been added to this course yet."
                )

            else:

                for content in contents:

                    with st.container(border=True):

                        col1, col2, col3 = st.columns(
                            [1, 5, 1]
                        )

                        with col1:

                            if content["content_type"] == "PDF":
                                st.write("📄")

                            else:
                                st.write("▶️")

                        with col2:

                            st.markdown(
                                f"**{content['title']}**"
                            )

                            st.caption(
                                f"Type: {content['content_type']}"
                            )

                            if content["source_url"]:

                                st.caption(
                                    content["source_url"]
                                )

                        with col3:

                            if st.button(
                                "Delete",
                                key=f"delete_{content['id']}",
                            ):

                                try:

                                    delete_content(
                                        content["id"]
                                    )

                                    st.success(
                                        "Content deleted."
                                    )

                                    st.rerun()

                                except Exception as e:

                                    st.error(
                                        f"Cannot delete content: {e}"
                                    )

    elif page == "Assessments":

        course_id = st.session_state.get(
            "selected_course_id"
        )

        course_title = st.session_state.get(
            "selected_course_title"
        )

        instructor_id = st.session_state.get("instructor_id")

        if course_id is None:

            st.warning(
                "Please open a course from the Dashboard first."
            )

        else:

            st.header(f"📝 Assessments — {course_title}")

            # --------------------------------
            # Create Assessment
            # --------------------------------

            st.subheader("➕ Create Assessment")

            title = st.text_input(
                "Assessment Title",
                placeholder="Example: DBMS Unit 1 Assessment",
            )

            description = st.text_area(
                "Description",
                placeholder="Assessment covering DBMS fundamentals.",
            )

            difficulty = st.selectbox(
                "Difficulty",
                ["EASY", "MEDIUM", "HARD"],
            )

            col1, col2 = st.columns(2)

            with col1:

                duration = st.number_input(
                    "Duration (minutes)",
                    min_value=1,
                    value=30,
                    step=5,
                )

            with col2:

                st.write("")

                st.write("")

                st.caption(
                    "Students will have this much time to complete the assessment."
                )

            st.markdown("#### Question Configuration")

            col1, col2 = st.columns(2)

            with col1:

                mcq_count = st.number_input(
                    "MCQ Questions",
                    min_value=0,
                    value=5,
                    step=1,
                )

            with col2:

                true_false_count = st.number_input(
                    "True/False Questions",
                    min_value=0,
                    value=5,
                    step=1,
                )

            total_questions = (
                mcq_count + true_false_count
            )

            st.info(
                f"Total questions: **{total_questions}**"
            )

            if st.button(
                "Create Assessment",
                type="primary",
            ):

                if not title.strip():

                    st.warning(
                        "Please enter an assessment title."
                    )

                elif total_questions == 0:

                    st.warning(
                        "Please select at least one question."
                    )

                else:

                    try:

                        assessment = create_assessment(
                            course_id=course_id,
                            created_by=instructor_id,
                            title=title,
                            description=description,
                            difficulty=difficulty,
                            duration_minutes=duration,
                            mcq_count=mcq_count,
                            true_false_count=true_false_count,
                        )

                        st.success(
                            f"Assessment '{assessment['title']}' created successfully!"
                        )

                        st.session_state.selected_assessment_id = (
                            assessment["id"]
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Failed to create assessment: {e}"
                        )

            st.divider()

            # --------------------------------
            # Existing Assessments
            # --------------------------------

            st.subheader("📋 Existing Assessments")

            try:

                assessments = get_course_assessments(
                    course_id=course_id,
                    instructor_id=instructor_id,
                )

                if not assessments:

                    st.info(
                        "No assessments have been created for this course."
                    )

                else:

                    for assessment in assessments:

                        with st.container(border=True):

                            st.markdown(
                                f"### 📝 {assessment['title']}"
                            )

                            st.caption(
                                f"Assessment ID: {assessment['id']} "
                                f"| Status: {assessment['status']}"
                            )

                            col1, col2, col3 = st.columns(3)

                            with col1:

                                st.write(
                                    f"**Difficulty:** "
                                    f"{assessment['difficulty']}"
                                )

                            with col2:

                                st.write(
                                    f"**Duration:** "
                                    f"{assessment['duration_minutes']} min"
                                )

                            with col3:

                                st.write(
                                    f"**Questions:** "
                                    f"{assessment['mcq_count']} MCQ + "
                                    f"{assessment['true_false_count']} T/F"
                                )
            except Exception as e:
                st.error(f"Failed to load assessments: {e}")

# -----------------------------
# Student Pages
# -----------------------------

else:

    if page == "Dashboard":

        st.header("Student Dashboard")

        st.info(
            "Student dashboard will be implemented later."
        )


    elif page == "My Assessments":

        st.header("My Assessments")

        st.info(
            "Student assessments will be implemented later."
        )