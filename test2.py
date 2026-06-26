import os
from transformers import pipeline
from PIL import Image

def run_captioning(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Target file not found: {image_path}")
        
    print(f"Generating visual caption for: {image_path}...")
    img = Image.open(image_path)
    
    captioner = pipeline(
        "image-text-to-text", 
        model="Salesforce/blip-image-captioning-base"
    )
    
    caption = captioner(img)
    return caption

if __name__ == "__main__":
    target_file = r"E:\INTERVIEW\WhatsApp Image 2026-06-20 at 4.20.43 PM.jpeg"
    result = run_captioning(target_file)
    print("Caption Output:", result)