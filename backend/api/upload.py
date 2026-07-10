from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from backend.models.document import Document
from backend.rag.ingest import IngestionService
from backend.services.document_service import create_document


router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".csv",
    ".xlsx",
    ".xls",
}


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = Form("default_user"),
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file uploaded."
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {extension}"
        )

    filename = Path(file.filename).name
    file_path = UPLOAD_DIR / filename

    contents = await file.read()

    with file_path.open("wb") as buffer:
        buffer.write(contents)

    ingestor = IngestionService()

    result = ingestor.ingest_file(
        str(file_path),
        user_id=user_id,
    )

    doc = Document(
        user_id=user_id,
        document_id=result["document_id"],
        filename=filename,
        vector_count=result["vectors_uploaded"],
    )

    mongo_id = await create_document(doc)

    result["mongo_document_id"] = mongo_id

    return result