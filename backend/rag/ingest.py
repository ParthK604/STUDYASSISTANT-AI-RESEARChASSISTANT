
import uuid

from backend.rag.loaders import load_document
from backend.rag.splitter import DocumentSplitter
from backend.rag.embeddings import EmbeddingService
from backend.rag.vectorstore import PineconeService



class IngestionService:
    """
    Handles the complete ingestion pipeline.

    File
      ↓
    Load
      ↓
    Split
      ↓
    Embed
      ↓
    Pinecone
    """

    def __init__(self):

        self.document_splitter = DocumentSplitter()

        self.embedding_service = EmbeddingService()

        self.vector_store = PineconeService()

    def ingest_file(
        self,
        file_path: str,
        user_id: str = "default_user",
    ) -> dict:

        # Step 1
        documents = load_document(file_path)

        # Step 2
        chunks = self.document_splitter.split(documents)

        # Step 3
        embeddings = self.embedding_service.embed_documents(chunks)

        # Step 4
        document_id = uuid.uuid4().hex

        uploaded = self.vector_store.upsert_documents(
            chunks=chunks,
            embeddings=embeddings,
            user_id=user_id,
            document_id=document_id,
        )

        return {
            "status": "success",
            "document_id": document_id,
            "chunks": len(chunks),
            "vectors_uploaded": uploaded,
        }


