import os
import uuid
import fitz  # PyMuPDF
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from google import genai
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Initialize Clients
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
gemini_client = genai.Client()

COLLECTION_NAME = "multimodal_rag_3072"

def recreate_collection():
    if qdrant.collection_exists(COLLECTION_NAME):
        print(f"Collection {COLLECTION_NAME} already exists. Deleting it...")
        qdrant.delete_collection(COLLECTION_NAME)
    
    print(f"Creating collection {COLLECTION_NAME}...")
    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
    )
    print("Collection created.")

def get_gemini_embedding(text):
    response = gemini_client.models.embed_content(
        model="gemini-embedding-2",
        contents=text
    )
    # The output structure is typically a list of embeddings.
    # response.embeddings[0].values
    try:
        return response.embeddings[0].values
    except AttributeError:
        # Fallback if structure is slightly different
        if hasattr(response, 'embeddings') and len(response.embeddings) > 0:
            if hasattr(response.embeddings[0], 'values'):
                return response.embeddings[0].values
        
        # If it's a dict
        if isinstance(response, dict) and "embeddings" in response:
            return response["embeddings"][0]["values"]
            
        print("Unexpected embedding response:", response)
        raise

def describe_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    prompt = "Describe this image in detail so it can be searched accurately."
    
    response = gemini_client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=[prompt, img]
    )
    return response.text

def process_pdf(pdf_path):
    print(f"Processing PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    points = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Extract Text
        text = page.get_text()
        if text.strip():
            print(f"Extracted text from page {page_num+1} (length: {len(text)})")
            vector = get_gemini_embedding(text)
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "page": page_num + 1,
                        "type": "text",
                        "content": text
                    }
                )
            )
            
        # Extract Images
        image_list = page.get_images(full=True)
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            
            try:
                print(f"Extracting and describing image from page {page_num+1}...")
                description = describe_image(image_bytes)
                print(f"Generated description: {description[:100]}...")
                
                vector = get_gemini_embedding(description)
                points.append(
                    PointStruct(
                        id=str(uuid.uuid4()),
                        vector=vector,
                        payload={
                            "page": page_num + 1,
                            "type": "image",
                            "content": description
                        }
                    )
                )
            except Exception as e:
                print(f"Error processing image on page {page_num+1}: {e}")

    return points

if __name__ == "__main__":
    pdf_path = r"E:\INTERVIEW\LORA RESRC.pdf"
    
    # Create Qdrant collection
    recreate_collection()
    
    # Process PDF and get points
    points = process_pdf(pdf_path)
    
    # Upsert points
    if points:
        print(f"Upserting {len(points)} points to Qdrant...")
        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        print("Indexing complete!")
    else:
        print("No data extracted from PDF.")
