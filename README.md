# GenLab AI Bot

This is a Retrieval-Augmented Generation (RAG) backend API I built using FastAPI. It lets you upload PDF documents, index them into a Qdrant vector database using local Ollama embeddings, and then ask questions about those documents.

It uses Groq for the LLM to keep inference super fast, while saving on embedding costs by running them locally with Ollama.

## Tech Stack
* **API Framework**: FastAPI
* **Orchestration**: LangChain
* **LLM**: Groq (`llama-3.3-70b-versatile`)
* **Embeddings**: Ollama (`nomic-embed-text` by default)
* **Vector DB**: Qdrant

## Prerequisites

Make sure you have the following installed before running this:

1. **Python 3.10+**
2. **Docker & Docker Compose**: Required for orchestrating the Qdrant vector database and the FastAPI backend.
3. **Ollama**: Installed and running locally. Run `ollama pull nomic-embed-text` to get the embedding model.
4. **Qdrant**: Runs via Docker Compose or use a Qdrant Cloud cluster.
5. **Groq API Key**: Grab one from the Groq console.

## Environment Variables

Create a `.env` file in the root directory and add the following:

```env
GROQ_API_KEY=your_groq_api_key_here
QDRANT_URL=http://qdrant:6333
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION=GenLab
EMBEDDING_MODEL=nomic-embed-text
OLLAMA_BASE_URL=[http://host.docker.internal:11434](http://host.docker.internal:11434)
