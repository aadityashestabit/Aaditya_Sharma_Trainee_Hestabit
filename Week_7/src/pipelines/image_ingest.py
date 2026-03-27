from pathlib import Path
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import faiss
import numpy as np
import json
import os
from src.embeddings.clip_embedder import embed_image

IMAGE_DIR     = "src/data/images"
VECTORSTORE_DIR = "src/vectorstore"
TEMP_DIR      = "src/data/images/temp_pdf_pages"
SUPPORTED     = {".png", ".jpg", ".jpeg", ".webp"}

# load BLIP once at module level
print("Loading BLIP captioning model...")
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model     = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model.eval()
print("BLIP model loaded.")

os.makedirs(VECTORSTORE_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

def extract_ocr(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        text  = pytesseract.image_to_string(image).strip()
        return text if text else ""
    except Exception as e:
        print(f"OCR failed for {image_path}: {e}")
        return ""

def generate_caption(image_path):
    try:
        image  = Image.open(image_path).convert("RGB")
        inputs = blip_processor(image, return_tensors="pt")
        with torch.no_grad():
            output = blip_model.generate(**inputs, max_new_tokens=50)
        return blip_processor.decode(output[0], skip_special_tokens=True)
    except Exception as e:
        print(f"Captioning failed for {image_path}: {e}")
        return ""

def collect_image_paths():
    image_paths = []

    # collect normal images
    for p in Path(IMAGE_DIR).rglob("*"):
        if p.suffix.lower() in SUPPORTED:
            if "temp_pdf_pages" not in str(p):
                image_paths.append(p)

    # convert scanned PDFs page by page
    for pdf_path in Path(IMAGE_DIR).rglob("*.pdf"):
        print(f"Converting scanned PDF: {pdf_path.name}")
        try:
            pages = convert_from_path(str(pdf_path), dpi=200)
            for page_num, page_image in enumerate(pages):
                page_path = Path(TEMP_DIR) / f"{pdf_path.stem}_page{page_num+1}.png"
                page_image.save(str(page_path))
                image_paths.append(page_path)
                print(f"  Converted page {page_num+1}/{len(pages)}")
        except Exception as e:
            print(f"Failed to convert {pdf_path.name}: {e}")

    return image_paths

def ingest():
    image_paths = collect_image_paths()

    if not image_paths:
        print(f"No images found in {IMAGE_DIR}")
        print("Add PNG, JPG or scanned PDF files to src/data/images/")
        return

    # clear old index
    for old_file in ["image_index.faiss", "image_store.json"]:
        old_path = f"{VECTORSTORE_DIR}/{old_file}"
        if os.path.exists(old_path):
            os.remove(old_path)
            print(f"Cleared {old_file}")

    print(f"Found {len(image_paths)} images. Processing...")

    all_vectors   = []
    all_texts     = []
    all_metadatas = []

    for idx, image_path in enumerate(image_paths):
        print(f"\n[{idx+1}/{len(image_paths)}] {image_path.name}")

        ocr_text = extract_ocr(str(image_path))
        print(f"  OCR: {ocr_text[:80]}..." if ocr_text else "  OCR: (no text found)")

        caption = generate_caption(str(image_path))
        print(f"  Caption: {caption}")

        clip_vector   = embed_image(str(image_path))
        combined_text = f"Caption: {caption}\nOCR Text: {ocr_text}".strip()

        is_pdf_page   = "temp_pdf_pages" in str(image_path)
        original_pdf  = image_path.name.rsplit("_page", 1)[0] + ".pdf" if is_pdf_page else ""

        all_vectors.append(clip_vector)
        all_texts.append(combined_text)
        all_metadatas.append({
            "image_path":   str(image_path),
            "filename":     image_path.name,
            "caption":      caption,
            "ocr_text":     ocr_text[:500],
            "file_type":    "scanned_pdf_page" if is_pdf_page else image_path.suffix.lower(),
            "original_pdf": original_pdf
        })

    # build and save FAISS index
    vectors   = np.array(all_vectors, dtype=np.float32)
    index     = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    faiss.write_index(index, f"{VECTORSTORE_DIR}/image_index.faiss")

    # save texts and metadata
    with open(f"{VECTORSTORE_DIR}/image_store.json", "w") as f:
        json.dump({"texts": all_texts, "metadatas": all_metadatas}, f)

    # summary
    types = {}
    for m in all_metadatas:
        t = m["file_type"]
        types[t] = types.get(t, 0) + 1

    print(f"\nStored {len(image_paths)} images in FAISS")
    print(f"File types ingested: {types}")


if __name__ == "__main__":
    ingest()