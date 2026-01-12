# Multimodal RAG System using CLIP (Text + Image Search)

## Project Summary

This project is a **Multimodal Retrieval-Augmented Generation (RAG) system** that enables **semantic search across both text and images inside PDF documents**.
It uses the **CLIP vision–language model (`clip-ViT-B-32`)**, **ChromaDB vector database**, and **Streamlit** to retrieve relevant text passages and associated images based on natural language queries.

---
Link = https://genrative-ai-1.onrender.com

## Objective

Traditional search systems fail to understand the **semantic relationship between text and images** in documents like research papers.
This project solves that problem by embedding **text and images into a shared vector space**, enabling intelligent cross-modal retrieval.

---

## How It Works (One Flow)

```
PDF Document
   ↓
Text Extraction + Image Extraction
   ↓
CLIP Embeddings (Text + Images)
   ↓
ChromaDB Vector Storage
   ↓
User Query (Natural Language)
   ↓
CLIP Query Embedding
   ↓
Similarity Search (Text + Images)
   ↓
Ranked Results via Streamlit UI
```

---

## Tech Stack

* **Language:** Python
* **Model:** CLIP (`clip-ViT-B-32`)
* **Embeddings:** Sentence-Transformers
* **Vector DB:** ChromaDB (Cloud)
* **PDF Parsing:** PyMuPDF (fitz)
* **Image Handling:** Pillow (PIL)
* **Frontend:** Streamlit
* **Deployment:** Render / Local

---

## Why `clip-ViT-B-32`?

* Pre-trained (no training required)
* Lightweight (~400 MB)
* Fast download and inference
* Stable with `sentence-transformers`
* Ideal for CI/CD and cloud deployment
* Strong performance for multimodal search

---

## Project Structure

```
├── ingest.py          # One-time PDF ingestion
├── rag_pipeline.py    # Query & retrieval logic
├── streamlit_app.py   # User interface
├── requirements.txt
├── sample_data/
│   └── attention-is-all-you-need.pdf
└── figures/           # Extracted images
```

---

## Core Components

### 1️⃣ Ingestion

* Extracts text blocks and images from PDF
* Links images with nearby captions
* Converts content into CLIP embeddings
* Stores embeddings in ChromaDB

### 2️⃣ Retrieval

* Converts user query into embedding
* Searches both text and image vectors
* Merges and ranks results by similarity

### 3️⃣ UI

* Accepts user questions
* Displays relevant text answers
* Shows related diagrams/images

---

## Example Queries

* *What is the Transformer architecture?*
* *Explain self-attention mechanism*
* *Show multi-head attention diagram*

---

## Output

For each query, the system returns:

*  Relevant text explanations
*  Related images/diagrams
*  Page numbers from the PDF

---

## Deployment Ready

* No model files stored in GitHub
* Models auto-download from Hugging Face
* Environment-variable–based configuration
* Fully compatible with Render CI/CD

---

## Future Scope

* LLM-based answer summarization
* Chat-style interface
* PDF page preview
* Cross-encoder reranking
* Multi-document support

---

## Key Takeaway

This project demonstrates a **real-world multimodal AI system** that combines **vision, language, and vector databases** to deliver intelligent document understanding.

---

### Author

**Mangesh Sambare**
Junior Data Scientist | Generative AI & Data Science

---
Just tell me 👍
