from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import os

class QdrantService:
    def __init__(self):
        # Connected to valid Qdrant instance
        self.client = QdrantClient(host="qdrant", port=6333)
        self.collection_name = "summarization_collection"
        self._ensure_collection()

    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )

    def upsert(self, points):
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, vector, top_k=5):
        return self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=top_k
        )

# Singleton
qdrant_service = QdrantService()
