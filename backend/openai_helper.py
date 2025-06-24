import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_faq(path: str = "data/faq.txt") -> str:
    with open(path, "r") as file:
        return file.read()

FAQ_CONTEXT = load_faq()

def get_response_from_openai(user_query: str) -> str:
    prompt = f"""
You are a helpful customer support agent. Answer the question based on the FAQ below.

FAQ:
{FAQ_CONTEXT}

Question: {user_query}
Answer:"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()
