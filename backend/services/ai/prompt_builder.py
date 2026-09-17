def build_question_generation_prompt(
    chunks: list[str],
    mcq_count: int,
    true_false_count: int,
    difficulty: str,
) -> str:
    """
    Build a compact prompt for generating assessment questions.
    """

    # Limit context for now.
    MAX_CONTEXT_CHARS = 10000

    context_parts = []
    current_length = 0

    for chunk in chunks:
      if current_length + len(chunk) > MAX_CONTEXT_CHARS:
        break

    context_parts.append(chunk)
    current_length += len(chunk)

    context = "\n\n".join(context_parts)
    print(f"Context size: {len(context)} characters")
    # max_chunks = 20
    # context = "\n\n".join(chunks[:max_chunks])

    prompt = f"""
Generate an assessment from the content below.

Requirements:
- Generate {mcq_count} MCQs and {true_false_count} True/False questions.
- Difficulty: {difficulty}.
- Use only the provided content.
- MCQs: exactly 4 options and 1 correct answer.
- True/False: exactly True and False options and 1 correct answer.
- Avoid duplicate questions.
- Include a brief explanation for each question.
- Return only valid JSON using this structure:

{{
  "questions": [
    {{
      "question_text": "...",
      "question_type": "MCQ",
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
    {{ "question_text": "...", "question_type": "TRUE_FALSE", "difficulty": "{difficulty}", "options": [ {{"option_text": "True", "is_correct": true}}, {{"option_text": "False", "is_correct": false}} ], "correct_answer": "True", "explanation": "..." }}
  ]
}}

CONTENT:
{context}
"""

    return prompt.strip()
