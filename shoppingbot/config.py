import os
from dotenv import load_dotenv

load_dotenv(override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Paths
BASE_DIR          = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PRODUCT_PATH = os.path.join(BASE_DIR, "data", "products.db")
DATA_TEXT_PATH    = os.path.join(BASE_DIR, "data", "policy.txt")
STORE_DIRECTORY   = os.path.join(BASE_DIR, "data", "faiss_store")

# Lazy load embeddings — only when needed
_EMBEDDINGS = None

def get_embeddings():
    global _EMBEDDINGS
    if _EMBEDDINGS is None:
        from langchain_huggingface import HuggingFaceEmbeddings
        _EMBEDDINGS = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return _EMBEDDINGS

# Keep EMBEDDINGS for backward compatibility
EMBEDDINGS = None