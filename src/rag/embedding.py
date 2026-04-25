from src.config import config
import requests
import numpy as np
from typing import List, Optional

class LlamaEmbedding:
    """llama-server 嵌入模型客户端"""
    
    def __init__(self):
        self.base_url = config.embedding_base_url
        self.embed_dim = config.embedding_dim
        self.embedding_endpoint = f"{self.base_url}/embedding"
    
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

# 全局嵌入模型实例
embed_model = LlamaEmbedding()
