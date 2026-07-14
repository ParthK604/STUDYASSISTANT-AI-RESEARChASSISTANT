from typing import List

from backend.rag.embeddings import EmbeddingService
from backend.rag.vectorstore import PineconeService


class RAGRetriever:
    """
    Retrieves the most relevant document chunks
    from Pinecone for a given query.
    """

    def __init__(
        self,
        pinecone_service: PineconeService,
        embedding_service: EmbeddingService,
    ) -> None:

        self.pinecone_service = pinecone_service
        self.embedding_service = embedding_service

    def retrieve(
        self,
        query: str,
        user_id: str="default_id",
        top_k: int = 5,
        score_threshold: float = 0.0,
    ) -> List[dict]:

        query_embedding = self.embedding_service.embed_query(
            query
        )

        results = self.pinecone_service.similarity_search(
            query_embedding=query_embedding,
            user_id=user_id,
            top_k=top_k,
        )

        retrieved_documents = []

        for rank, match in enumerate(
            results["matches"],
            start=1,
        ):

            score = match["score"]

            if score < score_threshold:
                continue

            metadata = match.get(
                "metadata",
                {}
            )

            retrieved_documents.append(
                {
                    "id": match["id"],
                    "content": metadata.get(
                        "text",
                        ""
                    ),
                    "metadata": metadata,
                    "score": score,
                    "rank": rank,
                }
            )

        return retrieved_documents