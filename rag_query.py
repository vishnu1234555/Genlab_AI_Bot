import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from google import genai
from groq import Groq
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Initialize Clients
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
gemini_client = genai.Client()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

COLLECTION_NAME = "multimodal_rag_3072"

def get_gemini_embedding(text):
    response = gemini_client.models.embed_content(
        model="gemini-embedding-2",
        contents=text
    )
    try:
        return response.embeddings[0].values
    except AttributeError:
        # Fallback if structure is slightly different
        if hasattr(response, 'embeddings') and len(response.embeddings) > 0:
            if hasattr(response.embeddings[0], 'values'):
                return response.embeddings[0].values
        
        if isinstance(response, dict) and "embeddings" in response:
            return response["embeddings"][0]["values"]
            
        print("Unexpected embedding response:", response)
        raise

def query_rag(user_question):
    print(f"Embedding query: '{user_question}'")
    query_vector = get_gemini_embedding(user_question)
    
    print("Searching Qdrant...")
    search_results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=1
    ).points
    
    if not search_results:
        return "No relevant context found in the knowledge base."
    
    # Construct Context
    context_chunks = []
    for i, res in enumerate(search_results):
        payload = res.payload
        chunk_type = payload.get("type", "unknown")
        page = payload.get("page", "unknown")
        content = payload.get("content", "")
        
        context_chunks.append(f"--- [Match {i+1} - {chunk_type.upper()} on Page {page}] ---\n{content}")
        
    context_text = "\n\n".join(context_chunks)
    print("\n--- Retrieved Context ---\n", context_text)
    print("-------------------------\n")
    
    # Generate Answer with Groq
    prompt = f"""You are a helpful AI assistant. Use the following context retrieved from a document to answer the user's question. 
The context may contain direct text chunks or descriptions of images found in the document.

Context:
{context_text}

User Question: {user_question}

Answer:"""

    print("Generating response via Groq (llama-3.1-8b-instant)...")
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-8b-instant",
    )
    
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    test_question = "What is the main topic of the LORA resource?"
    
    try:
        answer = query_rag(test_question)
        print("\n=== FINAL ANSWER ===")
        print(answer)
        print("====================\n")
    except Exception as e:
        print(f"Error during RAG pipeline execution: {e}")
