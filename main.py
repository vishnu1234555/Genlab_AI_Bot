from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import sys

# Ensure utf-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')

# Import our existing RAG query function
try:
    from rag_query import query_rag
except ImportError as e:
    print(f"Error importing query_rag: {e}")
    query_rag = None

app = FastAPI(title="RAG Chat API")

# Define the request model
class ChatRequest(BaseModel):
    message: str

# Define the response model
class ChatResponse(BaseModel):
    reply: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not query_rag:
        raise HTTPException(status_code=500, detail="Backend RAG module not loaded.")
    
    try:
        # Call the existing RAG pipeline
        answer = query_rag(request.message)
        return ChatResponse(reply=answer)
    except Exception as e:
        print(f"Error during RAG query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
