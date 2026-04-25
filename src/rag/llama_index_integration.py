from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core.embeddings import BaseEmbedding
from typing import List, Optional
from src.config import config
import requests
import os

# 配置 PostgreSQL 向量存储
PGVECTOR_CONNECTION_STRING = config.db_connection_string

class LlamaServerEmbedding(BaseEmbedding):
    """llama-server 嵌入模型"""
    
    def __init__(self, base_url: str = None, embed_dim: int = None):
        self.base_url = base_url or config.embedding_base_url
        self.embed_dim = embed_dim or config.embedding_dim
        self.embedding_endpoint = f"{self.base_url}/embedding"
        super().__init__(model_name="llama-server-embedding", embed_dim=self.embed_dim)
    
    def _get_query_embedding(self, query: str) -> List[float]:
        """获取查询嵌入"""
        return self._get_embedding(query)
    
    def _get_text_embedding(self, text: str) -> List[float]:
        """获取文本嵌入"""
        return self._get_embedding(text)
    
    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """批量获取文本嵌入"""
        return [self._get_embedding(text) for text in texts]
    
    def _get_embedding(self, text: str) -> List[float]:
        """调用 llama-server 获取嵌入"""
        payload = {
            "content": text
        }
        
        response = requests.post(self.embedding_endpoint, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["embedding"]
    
    @classmethod
    def class_name(cls) -> str:
        return "LlamaServerEmbedding"

# 创建嵌入模型实例
embed_model = LlamaServerEmbedding()

# 文档处理和向量化
def process_documents(documents_dir: str):
    """
    处理文档并创建索引
    
    Args:
        documents_dir: 文档目录路径
        
    Returns:
        向量索引
    """
    # 读取文档
    documents = SimpleDirectoryReader(documents_dir).load_data()
    
    # 文档分块
    node_parser = SentenceSplitter(
        chunk_size=config.rag_chunk_size, 
        chunk_overlap=config.rag_chunk_overlap
    )
    nodes = node_parser.get_nodes_from_documents(documents)
    
    # 初始化向量存储
    vector_store = PGVectorStore(
        connection_string=PGVECTOR_CONNECTION_STRING,
        table_name=config.db_table_name,
        embed_dim=config.embedding_dim
    )
    
    # 创建存储上下文
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # 创建索引
    index = VectorStoreIndex(
        nodes,
        storage_context=storage_context,
        embed_model=embed_model
    )
    
    return index

# 基于用户查询的向量检索
def query_index(index, query: str):
    """
    查询索引
    
    Args:
        index: 向量索引
        query: 查询内容
        
    Returns:
        查询结果
    """
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response
