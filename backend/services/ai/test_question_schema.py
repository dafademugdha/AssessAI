from backend.schemas.question import GeneratedQuestionResponse


data = {
    "questions": [
        {
            "question_text": "Which keyword is used to define a function in Python?",
            "question_type": "MCQ",
            "difficulty": "EASY",
            "options": [
                {
                    "option_text": "function",
                    "is_correct": False
                },
                {
                    "option_text": "def",
                    "is_correct": True
                },
                {
                    "option_text": "define",
                    "is_correct": False
                },
                {
                    "option_text": "fun",
                    "is_correct": False
                }
            ],
            "correct_answer": "def",
            "explanation": "The def keyword is used to define a function in Python."
        },
        {
            "question_text": "Python functions can accept parameters.",
            "question_type": "TRUE_FALSE",
            "difficulty": "EASY",
            "options": [
                {
                    "option_text": "True",
                    "is_correct": True
                },
                {
                    "option_text": "False",
                    "is_correct": False
                }
            ],
            "correct_answer": "True",
            "explanation": "Parameters allow values to be passed into a function."
        }
    ]
}


result = GeneratedQuestionResponse.model_validate(data)

print(result)
print("\nSchema validation successful!")