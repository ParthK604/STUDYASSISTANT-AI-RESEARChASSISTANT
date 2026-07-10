from pathlib import Path
from typing import List
import os

import numpy as np
from dotenv import load_dotenv
from langchain_core.documents import Document
from pinecone import Pinecone

# ==========================================
# Environment Variables
# ==========================================

env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(env_path)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")


class PineconeService:

    def __init__(self):

        self.pc = Pinecone(api_key=PINECONE_API_KEY)

        self.index = self.pc.Index(PINECONE_INDEX_NAME)

    def upsert_documents(
        self,
        chunks: List[Document],
        embeddings: np.ndarray,
        user_id: str,
        document_id: str,
    ) -> int:

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must match."
            )

        vectors = []

        for idx, (doc, embedding) in enumerate(
            zip(chunks, embeddings)
        ):

            vector_id = f"{document_id}_{idx}"

            metadata = {
                "text": doc.page_content,
                "user_id": user_id,
                "document_id": document_id,
                "source_file": doc.metadata.get("source_file", ""),
                "source_path": doc.metadata.get("source_path", ""),
                "file_type": doc.metadata.get("file_type", ""),
                "extension": doc.metadata.get("extension", ""),
                "page": doc.metadata.get("page", 0),
            }

            vectors.append(
                {
                    "id": vector_id,
                    "values": embedding.tolist(),
                    "metadata": metadata,
                }
            )

        self.index.upsert(vectors=vectors)

        return len(vectors)
    
    def similarity_search(
    self,
    query_embedding:np.ndarray,
    user_id: str,
    top_k: int = 5,
    ):

        return self.index.query(
            vector=query_embedding.tolist(),
            top_k=top_k,
            include_metadata=True,
            filter={
                "user_id": user_id
            }
        )