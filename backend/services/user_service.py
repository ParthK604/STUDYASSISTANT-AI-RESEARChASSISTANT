from datetime import datetime, UTC

from backend.db.mongo import db


async def sync_user(user_data: dict) -> dict:

    collection = db["users"]

    clerk_id = user_data["clerk_id"]
    now = datetime.now(UTC)

    payload = {
        "clerk_id": clerk_id,
        "email": user_data.get("email", ""),
        "name": user_data.get("name", ""),
        "provider": user_data.get("provider", "clerk"),
        "updated_at": now,
    }

    existing_user = await collection.find_one(
        {"clerk_id": clerk_id}
    )

    if existing_user:

        await collection.update_one(
            {"clerk_id": clerk_id},
            {"$set": payload},
        )

        updated_user = await collection.find_one(
            {"clerk_id": clerk_id}
        )

        updated_user["_id"] = str(updated_user["_id"])

        return {
            "user": updated_user,
            "created": False,
        }

    payload["created_at"] = now

    result = await collection.insert_one(payload)

    payload["_id"] = str(result.inserted_id)

    return {
        "user": payload,
        "created": True,
    }