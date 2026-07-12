from langgraph.graph import END

from backend.graph.state import AgentState


def route_after_agent(state: AgentState):

    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return END