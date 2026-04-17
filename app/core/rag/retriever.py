from langchain.tools import BaseTool
from langchain_mongodb import MongoDBAtlasVectorSearch
from app.storage.mongodb import mongo_storage


class Retriever(BaseTool):
    name: str = "retriever"
    description: str = "Tìm kiêm các đoạn văn bản có liên quan tới chủ đề bằng hàm cosin"
    vector_store: MongoDBAtlasVectorSearch = mongo_storage.get_vector_store("PTITHCM_vector")

    def _run(self, query: str, topk: int = 7) -> dict:
        """Thực hiện tìm kiếm thông tin trong cơ sở dữ liệu."""
        return {"results": self.vector_store.similarity_search(query, k=topk)}

    async def _arun(self, query: str, topk: int = 7) -> dict:
        """Thực hiện tìm kiếm thông tin (async)."""
        results = await self.vector_store.similarity_search(query, k=topk)
        return {"results": results}


retriever = Retriever()
