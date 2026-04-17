import os
import json
from typing import List, Dict
from langchain_community.document_loaders import PyPDFLoader, JSONLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.storage.mongodb import mongo_storage
from app.core.config.settings import settings
from app.core.rag.factory import LLMFactory

def metadata_func(record: dict, metadata: dict) -> dict:
    """Trích xuất metadata từ record JSON"""
    metadata["title"] = record.get("title", "")
    metadata["source_url"] = record.get("source_url", "")
    metadata["author"] = record.get("author", "")
    
    # Xử lý published_date nếu có
    pub_date = record.get("published_date")
    if isinstance(pub_date, dict) and "$date" in pub_date:
        metadata["published_date"] = pub_date["$date"]
    
    return metadata

def load_documents(directory: str) -> List[Document]:
    """Tải tất cả tài liệu từ thư mục data/"""
    print(f"--- Đang tải tài liệu từ {directory} ---")
    
    docs = []

    # 1. Loader cho PDF
    print("Đang quét các file PDF...")
    pdf_loader = DirectoryLoader(
        directory, 
        glob="./*.pdf", 
        loader_cls=PyPDFLoader
    )
    try:
        pdf_docs = pdf_loader.load()
        print(f"Đã tải {len(pdf_docs)} trang từ các file PDF.")
        docs.extend(pdf_docs)
    except Exception as e:
        print(f"Lỗi khi tải PDF: {e}")

    # 2. Loader cho JSON (documents.json)
    # documents.json là một list các object, mỗi object có trường 'content'
    json_path = os.path.join(directory, "documents.json")
    if os.path.exists(json_path):
        print(f"Đang nạp file {json_path}...")
        try:
            loader = JSONLoader(
                file_path=json_path,
                jq_schema='.[]',
                content_key='content',
                metadata_func=metadata_func
            )
            json_docs = loader.load()
            print(f"Đã tải {len(json_docs)} tài liệu từ file JSON.")
            docs.extend(json_docs)
        except Exception as e:
            print(f"Lỗi khi tải JSON: {e}")
    else:
        print("Không tìm thấy file documents.json")

    return docs

def split_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """Chia nhỏ tài liệu thành các đoạn văn bản (chunks)"""
    print(f"--- Đang chia nhỏ tài liệu: chunk_size={chunk_size}, overlap={chunk_overlap} ---")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Tổng cộng tạo ra {len(chunks)} đoạn văn bản.")
    return chunks

def ingest_data():
    """Quy trình nạp dữ liệu vào VectorDB"""
    data_dir = "./data"
    if not os.path.exists(data_dir):
        print(f"Thư mục {data_dir} không tồn tại.")
        return

    # 1. Load
    raw_docs = load_documents(data_dir)
    if not raw_docs:
        print("Không tìm thấy tài liệu nào để nạp.")
        return

    # 2. Split
    chunks = split_documents(raw_docs, chunk_size=1000, chunk_overlap=200)

    # 3. Initialize Vector Store
    print("--- Đang kết nối và nạp dữ liệu vào MongoDB Atlas Vector Search ---")
    # Sử dụng collection mặc định "PTITHCM_vector"
    collection_name = "PTITHCM_vector" 
    
    vector_store = mongo_storage.get_vector_store(collection_name=collection_name)

    # 4. Add to Vector Store
    # Chia nhỏ list chunks để nạp nếu số lượng quá lớn (tránh timeout hoặc giới hạn request)
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        vector_store.add_documents(batch)
        print(f"Đã nạp {min(i + batch_size, len(chunks))}/{len(chunks)} đoạn...")
    
    print(f"--- Hoàn tất! Đã nạp thành công {len(chunks)} đoạn vào collection '{collection_name}' ---")

if __name__ == "__main__":
    ingest_data()
