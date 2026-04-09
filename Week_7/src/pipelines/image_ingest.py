from pathlib import Path
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import pdfplumber
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import fitz
import os
from src.embeddings.clip_embedder import embed_image

BASE_DIR        = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VECTORSTORE_DIR = os.path.join(BASE_DIR, "src", "vectorstore")
IMAGE_DIR       = os.path.join(BASE_DIR, "src", "data", "images")
TEMP_DIR        = os.path.join(BASE_DIR, "src", "data", "images", "temp_pdf_pages")
SUPPORTED       = {".png", ".jpg", ".jpeg", ".webp"}

try:
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)
except:
    pass

def extract_ocr(image_path):
    try:
        return pytesseract.image_to_string(Image.open(image_path).convert("RGB")).strip()
    except:
        return ""

def generate_caption(image_path, blip_processor, blip_model):
    try:
        image  = Image.open(image_path).convert("RGB")
        inputs = blip_processor(image, return_tensors="pt")
        with torch.no_grad():
            output = blip_model.generate(**inputs, max_new_tokens=50)
        return blip_processor.decode(output[0], skip_special_tokens=True)
    except:
        return ""
    
def extract_images_from_pdf(pdf_path):
    extracted_paths = []
    try:
        doc = fitz.open(str(pdf_path))
    except:
        return extracted_paths

    try:
        for page_num in range(len(doc)):
            page   = doc[page_num]
            images = page.get_images(full=True)

            if not images:
                continue

            for img_idx, img in enumerate(images):
                xref = img[0]
                try:
                    base_image  = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    ext         = base_image["ext"]

                    width  = base_image["width"]
                    height = base_image["height"]
                    if width < 100 or height < 100:
                        continue

                    img_path = Path(TEMP_DIR) / f"{Path(pdf_path).stem}_p{page_num+1}_img{img_idx+1}.{ext}"
                    with open(str(img_path), "wb") as f:
                        f.write(image_bytes)

                    extracted_paths.append(img_path)
                    print(f"  Extracted image {img_idx+1} from page {page_num+1} — {width}x{height}px")

                except:
                    print(f"  Failed to extract image from page {page_num+1}")

        doc.close()
    except:
        pass

    return extracted_paths

def extract_pdf_text(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except:
        pass
    return text

def chunk_text(text, size=500):
    try:
        return [text[i:i+size] for i in range(0, len(text), size)]
    except:
        return []

def ingest():
    try:
        print("Loading BLIP model...")
        blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        blip_model     = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        blip_model.eval()

        print("Loading text embedding model...")
        text_model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Models loaded.")
    except:
        return

    image_vectors, image_texts, image_metadata = [], [], []
    text_vectors,  text_chunks, text_metadata  = [], [], []
    image_paths = []

    try:
        for p in Path(IMAGE_DIR).rglob("*"):
            if p.suffix.lower() in SUPPORTED and "temp_pdf_pages" not in str(p):
                image_paths.append(p)
    except:
        pass

    try:
        for pdf_path in Path(IMAGE_DIR).rglob("*.pdf"):
            print(f"\nProcessing PDF: {pdf_path.name}")

            pdf_text = extract_pdf_text(str(pdf_path))
            if pdf_text.strip():
                for chunk in chunk_text(pdf_text):
                    try:
                        text_vectors.append(text_model.encode(chunk))
                        text_chunks.append(chunk)
                        text_metadata.append({"source": str(pdf_path), "type": "pdf_text"})
                    except:
                        pass

            extracted = extract_images_from_pdf(str(pdf_path))
            if extracted:
                image_paths.extend(extracted)
                print(f"  Found {len(extracted)} images in {pdf_path.name}")
            else:
                print(f"  No embedded images found in {pdf_path.name}")
                try:
                    pages = convert_from_path(str(pdf_path), dpi=200)
                    for i, page in enumerate(pages):
                        page_path = Path(TEMP_DIR) / f"{pdf_path.stem}_page{i+1}.png"
                        page.save(str(page_path))
                        image_paths.append(page_path)
                        print(f"  Fallback: saved page {i+1} as image")
                except:
                    print(f"  Fallback also failed")
    except:
        pass

    print(f"\nProcessing {len(image_paths)} images...")
    for idx, image_path in enumerate(image_paths):
        try:
            print(f"[{idx+1}/{len(image_paths)}] {image_path.name}")

            ocr_text = extract_ocr(str(image_path))
            caption  = generate_caption(str(image_path), blip_processor, blip_model)
            vector   = embed_image(str(image_path))

            image_vectors.append(vector)
            image_texts.append(f"{caption} {ocr_text}".strip())
            image_metadata.append({
                "image_path": str(image_path),
                "caption":    caption,
                "ocr_text":   ocr_text[:500]
            })
        except:
            pass

    try:
        if image_vectors:
            vectors = np.array(image_vectors, dtype=np.float32)
            index   = faiss.IndexFlatL2(vectors.shape[1])
            index.add(vectors)
            faiss.write_index(index, f"{VECTORSTORE_DIR}/image_index.faiss")
            with open(f"{VECTORSTORE_DIR}/image_store.json", "w") as f:
                json.dump({"texts": image_texts, "metadatas": image_metadata}, f)
            print(f"Images indexed: {len(image_vectors)}")
    except:
        pass

    try:
        if text_vectors:
            vectors = np.array(text_vectors, dtype=np.float32)
            index   = faiss.IndexFlatIP(vectors.shape[1])
            index.add(vectors)
            faiss.write_index(index, f"{VECTORSTORE_DIR}/text_index.faiss")
            with open(f"{VECTORSTORE_DIR}/text_store.json", "w") as f:
                json.dump({"texts": text_chunks, "metadatas": text_metadata}, f)
            print(f"Text chunks indexed: {len(text_vectors)}")
    except:
        pass

    print("\nIngestion complete.")

if __name__ == "__main__":
    try:
        ingest()
    except:
        pass