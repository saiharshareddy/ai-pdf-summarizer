import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline

st.set_page_config(page_title="AI PDF Summarizer", layout="wide")
st.title("📄 AI PDF Summarizer")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    
    if len(text) < 100:
        st.warning("PDF is too short or empty.")
    else:
        st.subheader("Generating Summary...")
        summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")
        chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
        summary = ""
        for chunk in chunks:
            summary += summarizer(chunk, max_length=100, min_length=30, do_sample=False)[0]['summary_text'] + "\n"

        st.success("Summary Generated:")
        st.write(summary)
