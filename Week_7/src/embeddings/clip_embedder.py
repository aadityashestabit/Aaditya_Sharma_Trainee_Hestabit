import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import os

model_name = "openai/clip-vit-base-patch32"

try:
    model      = CLIPModel.from_pretrained(model_name)
    processor  = CLIPProcessor.from_pretrained(model_name)
    model.eval()
    print(f"CLIP model loaded: {model_name}")
except:
    model = None
    processor = None

def embed_image(image_path):
    try:
        image  = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            vision_outputs = model.vision_model(**inputs)
            features       = model.visual_projection(vision_outputs.pooler_output)
            features       = features / features.norm(dim=-1, keepdim=True)
        return features[0].tolist()
    except:
        return []

def embed_text(text):
    try:
        inputs = processor(
            text=[text], return_tensors="pt",
            padding=True, truncation=True, max_length=77
        )
        with torch.no_grad():
            text_outputs = model.text_model(**inputs)
            features     = model.text_projection(text_outputs.pooler_output)
            features     = features / features.norm(dim=-1, keepdim=True)
        return features[0].tolist()
    except:
        return []

if __name__ == "__main__":
    try:
        text_vec = embed_text("download speed test")
        print(f"Text embedding dim: {len(text_vec)}")

        test_images = [f for f in os.listdir("src/data/images")
                       if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg")]

        if test_images:
            img_vec = embed_image(f"src/data/images/{test_images[0]}")
            print(f"Image embedding dim: {len(img_vec)}")
            print(f"Dimensions match: {len(text_vec) == len(img_vec)}")
        else:
            print("No test image found in src/data/images/")
    except:
        pass