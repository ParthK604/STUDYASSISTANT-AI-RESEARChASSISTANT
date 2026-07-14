from typing import List

from backend.db.mongo import db
from backend.models.message import Message


async def create_message(
    message_data: Message,
) -> str:

    collection = db["messages"]

    result = await collection.insert_one(
        message_data.model_dump()
    )

    return str(result.inserted_id)


async def get_messages_by_user(
    user_id: str,
) -> List[dict]:

    collection = db["messages"]

    cursor = collection.find(
        {"user_id": user_id}
    ).sort("created_at", 1)

    messages = await cursor.to_list(
        length=1000
    )

    for message in messages:
        message["_id"] = str(message["_id"])

    return messages


async def delete_messages_by_user(
    user_id: str,
) -> bool:

    collection = db["messages"]

    result = await collection.delete_many(
        {"user_id": user_id}
    )

    return result.deleted_count > 0

async def get_recent_messages_by_user(
    user_id: str,
    limit: int = 10,
) -> List[dict]:

    collection = db["messages"]

    cursor = (
        collection.find(
            {"user_id": user_id}
        )
        .sort("created_at", -1)
        .limit(limit)
    )

    messages = await cursor.to_list(
        length=limit
    )

    messages.reverse()

    for message in messages:
        message["_id"] = str(message["_id"])

    return messages