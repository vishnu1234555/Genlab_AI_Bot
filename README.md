# GenLab AI Bot

A Retrieval-Augmented Generation (RAG) backend API built with FastAPI. This application allows users to upload PDF documents, index their contents into a Qdrant vector database using local Ollama embeddings, and query the documents using a Groq-powered LLM.

## 🚀 Features

* **PDF Ingestion:** Upload and parse PDF documents on the fly.
* **Local Embeddings:** Generates vector embeddings locally using Ollama (`nomic-embed-text` by default) to save on API costs and ensure privacy.
* **Vector Storage:** Stores and retrieves document chunks using Qdrant.
* **High-Speed Inference:** Utilizes Groq's API (`llama-3.3-70b-versatile`) for incredibly fast and accurate answer generation based on retrieved context.
* **FastAPI Backend:** Fully asynchronous API with Swagger UI documentation.

## 🛠️ Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **Orchestration:** [LangChain](https://python.langchain.com/)
* **LLM:** [Groq](https://groq.com/) (`llama-3.3-70b-versatile`)
* **Embeddings:** [Ollama](https://ollama.com/)
* **Vector Database:** [Qdrant](https://qdrant.tech/)

## 📋 Prerequisites

Before running this project, ensure you have the following installed and set up:

1. **Python 3.10+**
2. **Ollama:** Installed and running locally or on a remote server. You must pull your preferred embedding model (e.g., `ollama pull nomic-embed-text`).
3. **Qdrant:** A Qdrant Cloud cluster or a local Docker instance running.
4. **Groq API Key:** Obtain an API key from the Groq console.


