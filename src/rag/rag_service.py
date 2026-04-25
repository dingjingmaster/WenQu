from src.config import config
import requests
from typing import List, Optional
import json

class RAGService:
    """RAG 服务类，使用 llama-server 提供嵌入和推理能力"""
    
    def __init__(self):
        self.base_url = config.embedding_base_url
        self.embedding_endpoint = f"{self.base_url}/embedding"
        self.completion_endpoint = f"{self.base_url}/completion"
        self.embed_dim = config.embedding_dim
    
    def get_embedding(self, text: str) -> List[float]:
        """
        获取文本的嵌入向量
        
        Args:
            text: 输入文本
            
        Returns:
            嵌入向量
        """
        payload = {
            "content": text
        }
        
        response = requests.post(self.embedding_endpoint, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["embedding"]
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        批量获取文本的嵌入向量
        
        Args:
            texts: 文本列表
            
        Returns:
            嵌入向量列表
        """
        return [self.get_embedding(text) for text in texts]
    
    def cosine_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        计算两个嵌入向量的余弦相似度
        
        Args:
            embedding1: 嵌入向量 1
            embedding2: 嵌入向量 2
            
        Returns:
            余弦相似度
        """
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        norm1 = sum(a * a for a in embedding1) ** 0.5
        norm2 = sum(a * a for a in embedding2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def generate_response(self, query: str, context: str) -> str:
        """
        基于上下文生成回复
        
        Args:
            query: 用户查询
            context: 相关文档上下文
            
        Returns:
            生成的回复
        """
        payload = {
            "prompt": f"""基于以下上下文回答用户问题：

上下文：
{context}

用户问题：{query}

请根据上下文内容回答问题，如果上下文中没有相关信息，请说明。

回答：""",
            "temperature": config.llm_temperature,
            "max_tokens": config.llm_max_tokens
        }
        
        response = requests.post(self.completion_endpoint, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("content", "")

# 全局 RAG 服务实例
rag_service = RAGService()
