import numpy as np
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")

def generate_embedding(text):
    embedding = model.encode(text, normalize_embeddings=True)
    if embedding.ndim == 2:
        embedding = embedding.squeeze(0) 
    return np.array(embedding, dtype=np.float32)