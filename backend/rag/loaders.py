from pathlib import Path
from typing import Dict, Type

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    Docx2txtLoader,
)
from langchain_community.document_loaders.excel import (
    UnstructuredExcelLoader,
)


# ============================================
# Supported File Types
# ============================================

LOADERS: Dict[str, Type] = {
    ".pdf": PyPDFLoader,
    ".txt": TextLoader,
    ".csv": CSVLoader,
    ".docx": Docx2txtLoader,
    ".xlsx": UnstructuredExcelLoader,
    ".xls": UnstructuredExcelLoader,
}


# ============================================
# Load Single Document
# ============================================

def load_document(file_path: str) -> list[Document]:
    """
    Load a single document and convert it into
    LangChain Document objects.

    Supported formats:
        - PDF
        - TXT
        - CSV
        - DOCX
        - XLSX
        - XLS
    """

    path = Path(file_path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist.")

    extension = path.suffix.lower()

    if extension not in LOADERS:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    loader_class = LOADERS[extension]

    loader_kwargs = {}

    if extension == ".txt":
        loader_kwargs["encoding"] = "utf-8"

    loader = loader_class(
        str(path),
        **loader_kwargs
    )

    documents = loader.load()

    for doc in documents:

        doc.metadata.update(
            {
                "source_file": path.name,
                "source_path": str(path),
                "file_type": extension[1:].upper(),
                "extension": extension,
            }
        )

    return documents