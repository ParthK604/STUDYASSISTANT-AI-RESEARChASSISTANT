from langgraph.graph import StateGraph, START, END

from backend.graph.state import AgentState
from backend.graph.nodes import agent_node, tool_node
from backend.graph.router import route_after_agent


workflow = StateGraph(AgentState)

# Nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

# Start
workflow.add_edge(START, "agent")

# Agent decides where to go next
workflow.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "tools": "tools",
        END: END,
    },
)

# After a tool executes, return to the agent
workflow.add_edge("tools", "agent")

# Compile graph
app = workflow.compile()
