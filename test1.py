import os
from dotenv import load_dotenv
from google import genai
from PIL import Image

# Load environment variables from .env file
load_dotenv()

def run_gemini_vqa(image_path, query):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Target file not found: {image_path}")
        
    print(f"Initializing Gemini VLM processing for: {image_path}...")
    
    # 1. Initialize the Google GenAI client
    # The client automatically detects the GEMINI_API_KEY environment variable.
    client = genai.Client()
    
    # 2. Load the image into memory
    img = Image.open(image_path)
    
    # 3. Execute the multimodal request
    print(f"Query: {query}")
    print("Transmitting to Gemini API...")
    
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=[query, img]
    )
    
    return response.text

if __name__ == "__main__":
    # Your target Windows file path
    target_file = r"E:\INTERVIEW\WhatsApp Image 2026-06-20 at 4.20.43 PM.jpeg"
    test_query = "explain the whole flow of the image by explaining the image's intent"
    
    try:
        result = run_gemini_vqa(target_file, test_query)
        print("\n--- VLM OUTPUT ---")
        print(result)
        print("------------------\n")
    except Exception as e:
        print(f"\nExecution Failed: {e}")