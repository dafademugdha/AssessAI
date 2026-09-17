from backend.services.ai.llm_service import generate_with_llm


prompt = """
Generate one MCQ about Python functions.

Return only JSON:

{
  "question": "question here",
  "options": ["A", "B", "C", "D"],
  "correct_answer": "A"
}
"""


response = generate_with_llm(prompt)

print(response)