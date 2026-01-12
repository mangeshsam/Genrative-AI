# streamlit_app.py
import streamlit as st
from PIL import Image
from rag_pipeline import get_answer

st.set_page_config(page_title="Transformer RAG", layout="wide")
st.title("🤖 Transformer Q&A (Multimodal RAG)")

query = st.text_input("Ask a question about the Transformer paper")

if st.button("Search") and query:
    with st.spinner("Searching..."):
        results = get_answer(query)

    for i, r in enumerate(results, start=1):
        st.markdown(f"### Rank {i} | Page {r['page_number']}")

        if r["type"] == "text":
            st.write(r["content"])
        else:
            st.image(
                Image.open(r["image_path"]),
                caption=r["caption"],
                use_container_width=True
            )

        st.divider()
