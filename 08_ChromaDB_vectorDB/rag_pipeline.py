# rag_pipeline.py
import os
import chromadb
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer

FIG_COLLECTION_NAME = "attention_figures"
TEXT_COLLECTION_NAME = "attention_text_chunks"

client = chromadb.CloudClient(
  api_key='ck-GDUbzXXARSWT1JoFwsZNyF51Bp89RBzkVdzVmx3kXTbc',
  tenant='e313d9a7-5504-4844-8965-506a1c58e390',
  database='ChromaDB_image_text'
)
clip_model = SentenceTransformer("clip-ViT-B-32")

def embed_text(text: str) -> List[float]:
    return clip_model.encode([text], convert_to_numpy=True)[0].tolist()

def get_answer(
    query: str,
    top_k_text: int = 3,
    top_k_img: int = 1,
    top_k_overall: int = 4,
) -> List[Dict[str, Any]]:

    query_emb = embed_text(query)
    results = []

    text_col = client.get_collection(TEXT_COLLECTION_NAME)
    img_col = client.get_collection(FIG_COLLECTION_NAME)

    # ---- Text search ----
    text_res = text_col.query(
        query_embeddings=[query_emb],
        n_results=top_k_text,
        include=["documents", "metadatas", "distances"],
    )

    for doc, meta, dist in zip(
        text_res["documents"][0],
        text_res["metadatas"][0],
        text_res["distances"][0],
    ):
        results.append({
            "type": "text",
            "page_number": meta.get("page_number"),
            "content": doc,
            "distance": float(dist),
        })

    # ---- Image search ----
    img_res = img_col.query(
        query_embeddings=[query_emb],
        n_results=top_k_img,
        include=["documents", "metadatas", "distances"],
    )

    for doc, meta, dist in zip(
        img_res["documents"][0],
        img_res["metadatas"][0],
        img_res["distances"][0],
    ):
        results.append({
            "type": "image",
            "page_number": meta.get("page_number"),
            "image_path": meta.get("image_path"),
            "caption": meta.get("caption", ""),
            "content": doc,
            "distance": float(dist),
        })

    results.sort(key=lambda x: x["distance"])
    return results[:top_k_overall]
