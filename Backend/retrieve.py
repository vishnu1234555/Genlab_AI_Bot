from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings
from llm import llm
from dotenv import load_dotenv
import os


load_dotenv()

embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
base_url = os.getenv("OLLAMA_BASE_URL")  # e.g. http://host.docker.internal:11434
embeddings = OllamaEmbeddings(model=embedding_model, base_url=base_url) if base_url else OllamaEmbeddings(model=embedding_model)

api_key = os.getenv("QDRANT_API_KEY")
if not api_key:
    raise RuntimeError("QDRANT_API_KEY is not set. Put it in a .env file.")

url = os.getenv("QDRANT_URL")
if not url:
    raise RuntimeError("QDRANT_URL is not set. Put it in a .env file.")

collection = os.getenv("QDRANT_COLLECTION", "GenLab")
qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name=collection,
    url=url,
    api_key=api_key,
)


def build_prompt(context: str, question: str) -> str:
    return f"""Use the following context to answer the question. If the context doesn't contain enough information, say so. Otherwise give a clear, direct answer.

Context:
{context}

Question: {question}

Answer:"""


def retrieve_and_answer(question: str) -> str:
    results = qdrant.similarity_search(question, k=4)
    context = "\n\n".join(doc.page_content for doc in results)

    prompt = build_prompt(context=context, question=question)
    response = llm(prompt)
    return response


def main() -> None:
    question = input("Enter your question: ")
    answer = retrieve_and_answer(question)
    print(answer)


if __name__ == "__main__":
    main()