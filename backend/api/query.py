from fastapi import APIRouter
from pydantic import BaseModel

from backend.llm.groq import LLMService
from backend.models.message import Message
from backend.rag.embeddings import EmbeddingService
from backend.rag.retriever import RAGRetriever
from backend.rag.vectorstore import PineconeService
from backend.services.message_service import create_message


routerq = APIRouter()


class QueryRequest(BaseModel):
    user_id: str = "default_user"
    question: str


@routerq.post("/query")
async def generate_query(req: QueryRequest):

    embedder = EmbeddingService()
    pinecone = PineconeService()

    retriever = RAGRetriever(
        pinecone_service=pinecone,
        embedding_service=embedder,
    )

    llm_service = LLMService()

    # Store user message
    user_msg = Message(
        user_id=req.user_id,
        role="user",
        content=req.question,
    )

    user_message_id = await create_message(user_msg)

    # Generate answer
    llm_reply = llm_service.generate_answer(
        query=req.question,
        retriever=retriever,
        user_id=req.user_id,
    )

    # Store assistant message
    assistant_msg = Message(
        user_id=req.user_id,
        role="assistant",
        content=llm_reply,
    )

    assistant_message_id = await create_message(
        assistant_msg
    )

    return {
        "user_message_id": user_message_id,
        "assistant_message_id": assistant_message_id,
        "answer": llm_reply,
    }