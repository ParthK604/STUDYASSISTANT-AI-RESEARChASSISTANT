from langchain_core.messages import (
    AIMessage,
    HumanMessage,
)

from backend.graph.graph import app
from backend.services.message_service import (
    create_message,
    get_recent_messages_by_user,
)
from backend.models.message import Message
from backend.guardrails.guardrail_service import (validate_agent_input,validate_agent_output,validate_iterations)


async def run_agent(
    user_id: str,
    query: str,
) -> dict:
    
    error = validate_agent_input(query)

    if error:
        return {
            "error": error
        }

    previous_messages = (
        await get_recent_messages_by_user(
            user_id=user_id,
            limit=10,
        )
    )

    langchain_messages = []

    for message in previous_messages:

        if message["role"] == "user":

            langchain_messages.append(
                HumanMessage(
                    content=message["content"]
                )
            )

        else:

            langchain_messages.append(
                AIMessage(
                    content=message["content"]
                )
            )

    langchain_messages.append(
        HumanMessage(content=query)
    )

    state = {
        "user_query": query,
        "messages": langchain_messages,
        "tool_calls": [],
        "tool_results": [],
        "final_answer": "",
        "iterations": 0,
    }

    if not validate_iterations(state["iterations"]):
        return {
            "error": "Maximum agent iterations exceeded."
        }

    result = app.invoke(state)

    final_answer = (
        result["messages"][-1].content
    )

    error = validate_agent_output(
        final_answer
    )

    if error:
        return {
            "error": error
        }

    await create_message(
        Message(
            user_id=user_id,
            role="user",
            content=query,
        )
    )

    await create_message(
        Message(
            user_id=user_id,
            role="assistant",
            content=final_answer,
        )
    )

    return {
        "answer": final_answer,
    }