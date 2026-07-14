import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
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
tools = registry.get_all_tools()


SYSTEM_PROMPT = """You are a helpful study assistant with access to tools.

Use a tool whenever it is the best way to answer the user's request:
- rag_tool for questions about uploaded or local study documents
- tavily_tool for current events, web facts, or anything that needs live search
- calculator_tool for math, arithmetic, or exact calculations

If a tool is relevant, call it instead of answering from memory. If no tool is needed, answer directly.
"""


# ==========================================
# LLM
# ==========================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=groq_api_key,
    temperature=0,
)

llm_with_tools = llm.bind_tools(
    tools,
    tool_choice="auto",
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

    messages = [SystemMessage(content=SYSTEM_PROMPT), *state["messages"]]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


# ==========================================
# Tool Node
# ==========================================

tool_node = ToolNode(
    tools
)