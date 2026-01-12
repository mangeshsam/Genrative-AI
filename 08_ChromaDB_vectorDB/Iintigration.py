# ingest.py
import os
import fitz
import chromadb
import numpy as np
from PIL import Image
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer

# ---------------- CONFIG ----------------
PDF_PATH = "sample_data/attention-is-all-you-need.pdf"
FIGURES_DIR = "figures"

FIG_COLLECTION_NAME = "attention_figures"
TEXT_COLLECTION_NAME = "attention_text_chunks"

os.makedirs(FIGURES_DIR, exist_ok=True)

# ---------------- CHROMA CLIENT ----------------
client = chromadb.CloudClient(
  api_key='ck-GDUbzXXARSWT1JoFwsZNyF51Bp89RBzkVdzVmx3kXTbc',
  tenant='e313d9a7-5504-4844-8965-506a1c58e390',
  database='ChromaDB_image_text'
)

# ---------------- MODEL ----------------
clip_model = SentenceTransformer("clip-ViT-B-32")

def embed_text(text: str) -> List[float]:
    return clip_model.encode([text], convert_to_numpy=True)[0].tolist()

def embed_image(path: str) -> List[float]:
    img = Image.open(path).convert("RGB")
    return clip_model.encode([img], convert_to_numpy=True)[0].tolist()

# ---------------- OPEN PDF ----------------
doc = fitz.open(PDF_PATH)

image_records = []
text_records = []

# ---------------- EXTRACT DATA ----------------
for page_index, page in enumerate(doc, start=1):
    blocks = page.get_text("blocks")
    text_blocks = [b for b in blocks if b[4].strip()]
    images = page.get_images(full=True)

    # ---- Images ----
    for img_index, img in enumerate(images, start=1):
        xref = img[0]
        rects = page.get_image_rects(xref)
        if not rects:
            continue

        rect = rects[0]
        below = [b for b in text_blocks if b[1] >= rect.y1]
        caption = ""
        if below:
            caption = min(below, key=lambda b: abs(b[1] - rect.y1))[4].strip()

        img_data = doc.extract_image(xref)
        img_path = f"{FIGURES_DIR}/page_{page_index:02d}_img_{img_index}.png"

        with open(img_path, "wb") as f:
            f.write(img_data["image"])

        image_records.append({
            "id": f"p{page_index}_img{img_index}",
            "page_number": page_index,
            "image_path": img_path,
            "caption": caption,
        })

    # ---- Text ----
    for block_idx, b in enumerate(blocks):
        text = b[4].strip()
        if len(text) >= 80:
            text_records.append({
                "id": f"p{page_index}_block{block_idx}",
                "page_number": page_index,
                "text": text,
            })

# ---------------- STORE IN CHROMA ----------------
fig_collection = client.get_or_create_collection(FIG_COLLECTION_NAME)
text_collection = client.get_or_create_collection(TEXT_COLLECTION_NAME)

# Images
for rec in image_records:
    fig_collection.add(
        ids=[rec["id"]],
        embeddings=[embed_image(rec["image_path"])],
        documents=[rec["caption"]],
        metadatas=[{
            "page_number": rec["page_number"],
            "image_path": rec["image_path"],
            "caption": rec["caption"],
        }]
    )

# Text
for rec in text_records:
    text_collection.add(
        ids=[rec["id"]],
        embeddings=[embed_text(rec["text"])],
        documents=[rec["text"]],
        metadatas=[{
            "page_number": rec["page_number"]
        }]
    )

print("✅ Ingestion completed successfully")
