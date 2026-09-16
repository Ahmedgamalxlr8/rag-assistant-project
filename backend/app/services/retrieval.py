import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings
from app.utils.logging_config import logger

class VectorStoreService:
    def __init__(self):
        self.client = None
        self.collection = None

    def initialize(self):
        """Called once when FastAPI starts up."""
        logger.info(f"Loading persistent Chroma store from: {settings.CHROMA_DIR}")
        embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.EMBEDDING_MODEL
        )
        self.client = chromadb.PersistentClient(path=str(settings.CHROMA_DIR))
        self.collection = self.client.get_collection(
            name=settings.COLLECTION_NAME,
            embedding_function=embedding_func
        )
        logger.info(f"Ready: Loaded collection '{settings.COLLECTION_NAME}' ({self.collection.count()} chunks)")

    def retrieve(self, query: str, top_k: int = None) -> list[dict]:
        k = top_k or settings.TOP_K
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )
        
        chunks = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            chunks.append({
                "text": doc,
                "source": meta["source"],
                "page": meta["page"],
                "distance": dist
            })
        return chunks

vector_service = VectorStoreService()