from langchain_core.tools import tool

from backend.rag.embeddings import EmbeddingService
from backend.rag.retriever import RAGRetriever
from backend.rag.vectorstore import PineconeService


pinecone_service = PineconeService()
embedding_service = EmbeddingService()

retriever = RAGRetriever(
    pinecone_service=pinecone_service,
    embedding_service=embedding_service,
)


@tool
def rag_tool(
    query: str,
    user_id: str = "default_user",
) -> str:
    """
    Search uploaded documents using semantic search.
    """

    retrieved_chunks = retriever.retrieve(
        query=query,
        user_id=user_id,
    )

    if not retrieved_chunks:
        return "No relevant information found."

    context = "\n\n".join(
        chunk["content"]
        for chunk in retrieved_chunks
    )

    return context