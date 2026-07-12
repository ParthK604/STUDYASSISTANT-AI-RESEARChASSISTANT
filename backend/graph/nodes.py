import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode

from backend.graph.state import AgentState
from backend.tools.tool_registry import registry


# ==========================================
# Environment
# ==========================================

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

groq_api_key = os.getenv("GROQ_API_KEY")


# ==========================================
# LLM
# ==========================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=groq_api_key,
    temperature=0,
)

llm_with_tools = llm.bind_tools(
    registry.get_all_tools()
)


# ==========================================
# Agent Node
# ==========================================

def agent_node(state: AgentState):
    """
    Runs the LLM.

    The LLM decides whether it can answer directly
    or whether it needs to call one or more tools.
    """

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# ==========================================
# Tool Node
# ==========================================

tool_node = ToolNode(
    registry.get_all_tools()
)