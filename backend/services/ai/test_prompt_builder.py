from backend.services.ai.prompt_builder import (
    build_question_generation_prompt
)


chunks = [
    "Python functions are reusable blocks of code.",
    "Functions are defined using the def keyword.",
    "Parameters allow data to be passed into functions.",
]


prompt = build_question_generation_prompt(
    chunks=chunks,
    mcq_count=2,
    true_false_count=1,
    difficulty="MEDIUM",
)


print(prompt)