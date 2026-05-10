import os
from typing import List
from langchain.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from shoppingbot.config import get_embeddings
EMBEDDINGS = get_embeddings()

class VectorStoreManager:
    def __init__(self):
        self.embeddings = EMBEDDINGS
        self.store_dir  = STORE_DIRECTORY
        self.data_path  = DATA_TEXT_PATH
        self.vectorstore = self._load_or_create()

    def _exists(self) -> bool:
        return os.path.exists(os.path.join(self.store_dir, "index.faiss"))

    def _load(self):
        return FAISS.load_local(
            self.store_dir, self.embeddings,
            allow_dangerous_deserialization=True
        )

    def _create(self):
        loader = TextLoader(self.data_path, encoding='utf-8')
        docs   = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks   = splitter.split_documents(docs)
        vs = FAISS.from_documents(chunks, self.embeddings)
        os.makedirs(self.store_dir, exist_ok=True)
        vs.save_local(self.store_dir)
        return vs

    def _load_or_create(self):
        if self._exists():
            return self._load()
        return self._create()

    def search(self, query: str, k: int = 3) -> List[str]:
        results = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in results]


@tool
def policy_search_tool(query: str) -> str:
    """
    Search for store policies, return/exchange policies, shipping information,
    warranty details, or any other store rules and guidelines.
    Use this when a customer asks about policies, shipping, returns, refunds, or store rules.
    """
    try:
        manager = VectorStoreManager()
        results = manager.search(query)
        if not results:
            return "No policy information found for that query."
        return "\n\n".join(results)
    except Exception as e:
        return f"Error searching policies: {str(e)}"
