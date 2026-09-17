import json

from backend.services.ai.prompt_builder import (
    build_question_generation_prompt
)

from backend.services.ai.llm_service import (
    generate_with_llm
)

from backend.schemas.question import (
    GeneratedQuestionResponse
)


chunks = [
    "Python functions are reusable blocks of code.",
    "Functions are defined using the def keyword.",
    "Parameters allow data to be passed into functions.",
    "The return statement is used to return a value from a function."
]


prompt = build_question_generation_prompt(
    chunks=chunks,
    mcq_count=2,
    true_false_count=1,
    difficulty="EASY"
)


response = generate_with_llm(prompt)

print("\nRAW LLM RESPONSE:")
print(response)


try:
    data = json.loads(response)

    validated_response = GeneratedQuestionResponse.model_validate(data)

    print("\nVALIDATION SUCCESSFUL!")

    print(
        f"Generated {len(validated_response.questions)} questions."
    )

    for i, question in enumerate(
        validated_response.questions,
        start=1
    ):
        print(f"\nQuestion {i}:")
        print(question.question_text)
        print("Type:", question.question_type)
        print("Difficulty:", question.difficulty)
        print("Correct answer:", question.correct_answer)

except json.JSONDecodeError:
    print("\nERROR: LLM did not return valid JSON.")

except Exception as e:
    print("\nVALIDATION ERROR:")
    print(e)

