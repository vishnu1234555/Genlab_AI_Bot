from langchain_community.document_loaders import PyPDFLoader
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
import os


load_dotenv()  # load variables from .env if present


def index_pdf(file_path: str | None = None) -> dict:
    """
    Load a PDF, create embeddings, and upsert into Qdrant.
    Returns a small status dict for API/CLI use.
    """
    if file_path is None:
        file_path = r"c:\Users\DELL\AppData\Roaming\Cursor\User\workspaceStorage\51149e7cd9206e6d61c16ace5011d2f2\pdfs\1898273e-ca90-4478-ba76-8306621ee129\Untitled document.pdf"

    loader = PyPDFLoader(file_path)
    docs = loader.load()

    url = os.getenv("QDRANT_URL")
    if not url:
        raise RuntimeError("QDRANT_URL is not set. Put it in a .env file.")
    api_key = os.getenv("QDRANT_API_KEY")
    if not api_key:
        raise RuntimeError("QDRANT_API_KEY is not set. Put it in a .env file.")

    embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    base_url = os.getenv("OLLAMA_BASE_URL")  # e.g. http://host.docker.internal:11434
    embeddings = OllamaEmbeddings(model=embedding_model, base_url=base_url) if base_url else OllamaEmbeddings(model=embedding_model)

    collection = os.getenv("QDRANT_COLLECTION", "GenLab")
    QdrantVectorStore.from_documents(
        docs,
        embeddings,
        url=url,
        api_key=api_key,
        collection_name=collection,
    )

    return {"message": "Indexed PDF into Qdrant", "documents_indexed": len(docs)}


if __name__ == "__main__":
    result = index_pdf()
    print(result)