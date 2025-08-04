from openai import OpenAI
from .config import OPENAI_API_KEY, BASE_URL, GPT_MODEL, MAX_TOKENS_RESPONSE, EMBEDDING_MODEL

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=BASE_URL
)

def get_embedding(text: str) -> list:
    """Get embedding for text"""
    response = client.embeddings.create(
        input=[text],
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding

def get_gpt_response(messages: list, max_tokens: int = MAX_TOKENS_RESPONSE) -> str:
    """Get response from GPT model"""
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=0,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content