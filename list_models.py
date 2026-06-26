from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

print("Listing models:")
try:
    models = client.models.list()
    for m in models:
        # Filtering for text-embedding models
        if 'embed' in m.name or 'text-embedding' in m.name:
            print(f"Name: {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
