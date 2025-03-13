import numpy as np
import os
import pickle
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


FAISS_INDEX_DIR =  "faiss_indexes"


embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1")

def store_in_faiss(user_id, chunks):
    index_path = os.path.join(FAISS_INDEX_DIR, f"faiss_index_user_{user_id}.pkl")

    if os.path.exists(index_path):
        with open(index_path, "rb") as f:
            faiss_index = pickle.load(f)
    else:
        faiss_index = None  
    
    if faiss_index is None:
        faiss_index = FAISS.from_texts(chunks, embedding_function)
    else:
        new_index = FAISS.from_texts(chunks, embedding_function)
        faiss_index.merge_from(new_index)

    with open(index_path, "wb") as f:
        pickle.dump(faiss_index, f)



def load_faiss(user_id):
    index_path = os.path.join(FAISS_INDEX_DIR, f"faiss_index_user_{user_id}.pkl")
    try:
        with open(index_path, "rb") as f:
            faiss_index = pickle.load(f)
        return faiss_index
    except FileNotFoundError:
        return None


def retrieve_relevant_chunks(user_id, query, top_k=3):

    faiss_index = load_faiss(user_id)
    if not faiss_index:
        return []
    results = faiss_index.similarity_search(query, k=top_k)

    return [doc.page_content for doc in results]