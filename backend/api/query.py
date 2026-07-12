from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.agent_service import run_agent


routerq = APIRouter()


class QueryRequest(BaseModel):
    user_id: str = "default_user"
    question: str


@routerq.post("/query")
async def query(req: QueryRequest):

    response = await run_agent(
        user_id=req.user_id,
        query=req.question,
    )

    return response["answer"]