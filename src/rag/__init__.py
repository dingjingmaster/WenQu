"""
RAG 模块
使用 llama-server 提供的 embedding 和推理能力
不再依赖 LlamaIndex、HuggingFace 等外部框架
"""
from .rag_service import rag_service, RAGService
from .embedding import LlamaEmbedding
from .db_config import engine, Base, SessionLocal, get_db
from .models import Document

__all__ = [
    "rag_service", 
    "RAGService", 
    "LlamaEmbedding",
    "engine", 
    "Base", 
    "SessionLocal", 
    "get_db",
    "Document"
]
