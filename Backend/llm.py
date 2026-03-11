from groq import Groq
from dotenv import load_dotenv
import os

_SYSTEM_CONTENT = "You are GenLab’s all-knowing assistant. Your main goal is to answer the user’s query clearly and directly."

load_dotenv()


def llm(prompt: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set. Put it in a .env file.")

    client = Groq(api_key=api_key)
    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": _SYSTEM_CONTENT},
            {"role": "user", "content": prompt},
        ],
    )
    return chat_completion.choices[0].message.content