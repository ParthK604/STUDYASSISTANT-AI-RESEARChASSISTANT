from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    user_query: str

    messages: Annotated[list[BaseMessage], add_messages]

    tool_calls: list[dict]

    tool_results: list[str]

    final_answer: str

    iterations: int