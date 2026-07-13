from langgraph.graph import END

from backend.graph.state import AgentState


def route_after_agent(state: AgentState):

    last_message = state["messages"][-1]
    tool_calls = getattr(last_message, "tool_calls", None)

    if not tool_calls:
        tool_calls = last_message.additional_kwargs.get("tool_calls", [])

    if tool_calls:
        return "tools"

    return END