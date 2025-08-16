import os
import re
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import faiss
import numpy as np
import pickle

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_MODEL = SentenceTransformer(MODEL_NAME)

def load_text_from_file(path):
    if path.lower().endswith('.pdf'):
        reader = PdfReader(path)
        return "\n".join(page.extract_text() for page in reader.pages)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def split_into_passages(text, max_tokens=300):
    # crude whitespace splitting; adapt tokenizer if needed
    sentences = re.split(r'(?<=[\.\?\!])\s+', text)
    passages, current = [], []
    count = 0
    for sent in sentences:
        toks = sent.split()
        if count + len(toks) > max_tokens:
            passages.append(" ".join(current))
            current, count = [], 0
        current.extend(toks)
        count += len(toks)
    if current:
        passages.append(" ".join(current))
    return passages

def embed_passages(passages):
    return EMBEDDING_MODEL.encode(passages, show_progress_bar=True, convert_to_numpy=True)

INDEX_FILE = os.path.join(os.path.dirname(__file__), 'faiss_index.bin')
METADATA_FILE = os.path.join(os.path.dirname(__file__), 'faiss_metadata.pkl')

def build_faiss_index(embeddings: np.ndarray, metadata: list):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    # persist index and metadata
    faiss.write_index(index, INDEX_FILE)
    with open(METADATA_FILE, 'wb') as f:
        pickle.dump(metadata, f)
    return index