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



async def run_agent(
    user_id: str,
    query: str,
) -> dict:
    
    

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

    

    result = app.invoke(state)

    final_answer = (
        result["messages"][-1].content
    )



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