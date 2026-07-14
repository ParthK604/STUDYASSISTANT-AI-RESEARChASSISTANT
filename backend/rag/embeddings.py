from typing import List

import numpy as np
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Generates embeddings for documents and queries.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:

        self.model = SentenceTransformer(model_name)

    def embed_documents(
        self,
        documents: List[Document],
    ) -> np.ndarray:
        """
        Generate embeddings for document chunks.
        """

        texts = [
            doc.page_content
            for doc in documents
        ]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
            normalize_embeddings=True,
        )

        return embeddings

    def embed_query(
        self,
        query: str,
    ) -> np.ndarray:
        """
        Generate embedding for a user query.
        """

        return self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )