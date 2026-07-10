from typing import List

from backend.db.mongo import db
from backend.models.document import Document


async def create_document(
    doc_data: Document,
) -> str:

    collection = db["documents"]

    result = await collection.insert_one(
        doc_data.model_dump()
    )

    return str(result.inserted_id)


async def get_documents_by_user(
    user_id: str,
) -> List[dict]:

    collection = db["documents"]

    cursor = collection.find(
        {"user_id": user_id}
    ).sort("created_at", -1)

    documents = await cursor.to_list(
        length=1000
    )

    for document in documents:
        document["_id"] = str(document["_id"])

    return documents


async def delete_document(
    document_id: str,
) -> bool:

    collection = db["documents"]

    result = await collection.delete_one(
        {"document_id": document_id}
    )

    return result.deleted_count > 0