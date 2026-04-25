import requests
import json
from src.config import config

class InferenceService:
    """推理服务类，负责与 llama-server 交互"""
    
    def __init__(self, base_url: str = None):
        """
        初始化推理服务
        
        Args:
            base_url: llama-server 服务的基础 URL，默认从配置文件读取
        """
        self.base_url = base_url or config.llm_base_url
        self.completion_endpoint = f"{self.base_url}/completion"
        self.chat_endpoint = f"{self.base_url}/chat/completions"
        self.temperature = config.llm_temperature
        self.max_tokens = config.llm_max_tokens
    
    def generate_completion(self, prompt: str, max_tokens: int = None, temperature: float = None) -> str:
        """
        生成文本补全
        
        Args:
            prompt: 输入提示词
            max_tokens: 最大生成 token 数
            temperature: 温度参数，控制随机性
            
        Returns:
            生成的文本
        """
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens or self.max_tokens,
            "temperature": temperature or self.temperature,
            "stop": ["</s>", "User:", "Assistant:"]
        }
        
        try:
            response = requests.post(self.completion_endpoint, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("content", "")
        except Exception as e:
            raise Exception(f"推理服务调用失败：{str(e)}")
    
    def generate_chat(self, messages: list, max_tokens: int = None, temperature: float = None) -> str:
        """
        生成聊天回复
        
        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "消息内容"}]
            max_tokens: 最大生成 token 数
            temperature: 温度参数，控制随机性
            
        Returns:
            生成的回复
        """
        payload = {
            "messages": messages,
            "max_tokens": max_tokens or self.max_tokens,
            "temperature": temperature or self.temperature
        }
        
        try:
            response = requests.post(self.chat_endpoint, json=payload)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            raise Exception(f"推理服务调用失败：{str(e)}")
    
    def health_check(self) -> bool:
        """
        检查推理服务是否可用
        
        Returns:
            True 表示服务可用，False 表示不可用
        """
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception:
            return False
