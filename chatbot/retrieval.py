import faiss, pickle
import numpy as np

from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_MODEL = SentenceTransformer(MODEL_NAME)
INDEX_FILE = 'chatbot/faiss_index.bin'
METADATA_FILE = 'chatbot/faiss_metadata.pkl'

# load once at startup
index = faiss.read_index(INDEX_FILE)
with open(METADATA_FILE, 'rb') as f:
    metadata = pickle.load(f)

def query_index(question: str, top_k=5):
    q_emb = EMBEDDING_MODEL.encode([question], convert_to_numpy=True)
    D, I = index.search(q_emb.astype(np.float32), top_k)
    results = []
    for dist, idx in zip(D[0], I):
        meta = metadata[idx]
        results.append({
            'score': float(dist),
            'doc_id': meta['doc_id'],
            'passage': meta['text']
        })
    return results
