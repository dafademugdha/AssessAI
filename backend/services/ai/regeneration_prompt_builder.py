def build_question_regeneration_prompt(
    chunks: list[str],
    existing_questions: list[str],
    question_type: str,
    difficulty: str,
) -> str:
    """
    Build a compact prompt for regenerating one question.
    """

    max_chunks = 20
    context = "\n\n".join(chunks[:max_chunks])

    existing_questions_text = "\n".join(
        f"- {question}"
        for question in existing_questions
    )

    prompt = f"""
Generate ONE replacement assessment question.

Requirements:
- Question type: {question_type}
- Difficulty: {difficulty}
- Use only the provided content.
- Do not repeat or closely paraphrase any existing question.
- The new question must test a different concept or aspect when possible.
- MCQ: exactly 4 options and 1 correct answer.
- TRUE_FALSE: exactly True and False options and 1 correct answer.
- Include a brief explanation.
- question_type must be exactly "MCQ" or "TRUE_FALSE".
- Return only valid JSON.

Format:
{{
  "questions": [
    {{
      "question_text": "...",
      "question_type": "{question_type}",
      "difficulty": "{difficulty}",
      "options": [
        {{"option_text": "...", "is_correct": false}},
        {{"option_text": "...", "is_correct": true}},
        {{"option_text": "...", "is_correct": false}},
        {{"option_text": "...", "is_correct": false}}
      ],
      "correct_answer": "...",
      "explanation": "..."
    }}
  ]
}}

EXISTING QUESTIONS TO AVOID:
{existing_questions_text}

CONTENT:
{context}
"""

    return prompt.strip()