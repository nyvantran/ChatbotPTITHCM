from pymongo import MongoClient
from app.core.config.settings import settings
from app.core.rag.factory import LLMFactory
from langchain_mongodb import MongoDBAtlasVectorSearch

class MongoStorage:
    def __init__(self):
        self._client = None

    @property
    def client(self) -> MongoClient:
        if self._client is None:
            self._client = MongoClient(settings.MONGODB_URL)
        return self._client

    def get_db(self):
        """Trả về database đồng bộ"""
        return self.client[settings.DATABASE_NAME]

    def get_vector_store(self, collection_name: str = "vectors"):
        return MongoDBAtlasVectorSearch(
            collection=self.client[settings.DATABASE_NAME][collection_name],
            embedding=LLMFactory.get_embeddings("huggingface"),
            index_name=settings.VECTOR_INDEX_NAME,
            relevance_score_fn="cosine",
        )

    def get_retriever(self, k: int = 5):
        return self.get_vector_store().as_retriever(search_kwargs={"k": k})

mongo_storage = MongoStorage()
vector_storage = mongo_storage
