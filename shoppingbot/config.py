import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv(override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Paths
BASE_DIR          = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PRODUCT_PATH = os.path.join(BASE_DIR, "data", "products.db")
DATA_TEXT_PATH    = os.path.join(BASE_DIR, "data", "policy.txt")
STORE_DIRECTORY   = os.path.join(BASE_DIR, "data", "faiss_store")

# Faster embeddings model
try:
    EMBEDDINGS = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
except Exception as e:
    print(f"Embeddings loading failed: {e}")
    EMBEDDINGS = None