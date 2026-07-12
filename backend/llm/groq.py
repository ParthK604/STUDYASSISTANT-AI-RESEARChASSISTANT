import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq

env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(env_path)

groq_api_key = os.getenv("GROQ_API_KEY")


class LLMService:

    def __init__(self):

        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama-3.1-8b-instant",
            temperature=0.1,
            max_tokens=1000,
        )

    def generate_answer(
        self,
        query: str,
        retriever,
        user_id: str = "default_user",
        top_k: int = 4,
    ):

        results = retriever.retrieve(
            query=query,
            user_id=user_id,
            top_k=top_k,
        )

        if not results:
            return "No relevant context found."

        context = "\n\n".join(
            doc["content"]
            for doc in results
        )

        prompt = f"""
You are a helpful study assistant.

Answer ONLY using the provided context.

Context:
{context}

Question:
{query}

Answer:
"""

        response = self.llm.invoke(prompt)

        return response.content


