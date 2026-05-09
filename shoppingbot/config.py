import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Paths
BASE_DIR          = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PRODUCT_PATH = os.path.join(BASE_DIR, "data", "products.db")
DATA_TEXT_PATH    = os.path.join(BASE_DIR, "data", "policy.txt")
STORE_DIRECTORY   = os.path.join(BASE_DIR, "data", "faiss_store")

# Free local embeddings — no API key needed, runs on CPU
# Downloads ~90MB model on first run, then cached locally
EMBEDDINGS = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)
