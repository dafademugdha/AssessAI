import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not configured.")


client = Groq(api_key=api_key)


def generate_with_llm(prompt: str) -> str:
    """
    Send a prompt to the LLM and return its response.
    """

    response = client.chat.completions.create(
        model="groq/compound",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.3,
        response_format={
            "type": "json_object"
        },
    )

    return response.choices[0].message.content