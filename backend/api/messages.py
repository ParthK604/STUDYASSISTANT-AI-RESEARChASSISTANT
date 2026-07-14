from fastapi import APIRouter, Query

from backend.services.message_service import get_messages_by_user


router = APIRouter()


@router.get("/messages")
async def messages(user_id: str = Query(...)):
    return await get_messages_by_user(user_id)