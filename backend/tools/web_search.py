import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient


env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(env_path)

tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def tavily_tool(
    query: str,
    max_results: int = 3,
    topic: Literal["general", "news"] = "general",
) -> str:
    """
    Search the web using Tavily.
    """

    response = tavily_client.search(
        query=query,
        max_results=max_results,
        topic=topic,
    )

    results = response.get("results", [])

    if not results:
        return "No web results found."

    output = []

    for result in results:

        output.append(
            f"Title: {result['title']}\n"
            f"Content: {result['content']}\n"
            f"URL: {result['url']}"
        )

    return "\n\n".join(output)