import configparser
import os
from typing import Optional

class Config:
    """配置管理类，负责加载和解析配置文件"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置类
        
        Args:
            config_path: 配置文件路径，默认为项目根目录的 config/config.ini
        """
        if config_path is None:
            # 获取项目根目录
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(project_root, "config", "config.ini")
        
        self.config = configparser.ConfigParser()
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在：{config_path}")
        
        self.config.read(config_path, encoding='utf-8')
        self.config_path = config_path
    
    # LLM 配置
    @property
    def llm_base_url(self) -> str:
        return self.config.get('llm', 'base_url', fallback='http://localhost:8080')
    
    @property
    def llm_temperature(self) -> float:
        return self.config.getfloat('llm', 'temperature', fallback=0.7)
    
    @property
    def llm_max_tokens(self) -> int:
        return self.config.getint('llm', 'max_tokens', fallback=1024)
    
    # Embedding 配置
    @property
    def embedding_base_url(self) -> str:
        return self.config.get('embedding', 'base_url', fallback='http://localhost:8080')
    
    @property
    def embedding_dim(self) -> int:
        return self.config.getint('embedding', 'embed_dim', fallback=768)
    
    # 数据库配置
    @property
    def db_host(self) -> str:
        return self.config.get('database', 'host', fallback='localhost')
    
    @property
    def db_port(self) -> int:
        return self.config.getint('database', 'port', fallback=5432)
    
    @property
    def db_name(self) -> str:
        return self.config.get('database', 'database', fallback='wenqu')
    
    @property
    def db_user(self) -> str:
        return self.config.get('database', 'user', fallback='postgres')
    
    @property
    def db_password(self) -> str:
        return self.config.get('database', 'password', fallback='postgres')
    
    @property
    def db_table_name(self) -> str:
        return self.config.get('database', 'table_name', fallback='documents')
    
    @property
    def db_connection_string(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    # 服务器配置
    @property
    def server_host(self) -> str:
        return self.config.get('server', 'host', fallback='0.0.0.0')
    
    @property
    def server_port(self) -> int:
        return self.config.getint('server', 'port', fallback=8000)
    
    @property
    def server_debug(self) -> bool:
        return self.config.getboolean('server', 'debug', fallback=False)
    
    # RAG 配置
    @property
    def rag_chunk_size(self) -> int:
        return self.config.getint('rag', 'chunk_size', fallback=1000)
    
    @property
    def rag_chunk_overlap(self) -> int:
        return self.config.getint('rag', 'chunk_overlap', fallback=200)
    
    def get(self, section: str, option: str, fallback: Optional[str] = None) -> str:
        """
        获取配置值
        
        Args:
            section: 配置节
            option: 配置项
            fallback: 默认值
            
        Returns:
            配置值
        """
        return self.config.get(section, option, fallback=fallback)
    
    def getint(self, section: str, option: str, fallback: Optional[int] = None) -> int:
        """获取整数配置值"""
        return self.config.getint(section, option, fallback=fallback)
    
    def getfloat(self, section: str, option: str, fallback: Optional[float] = None) -> float:
        """获取浮点数配置值"""
        return self.config.getfloat(section, option, fallback=fallback)
    
    def getboolean(self, section: str, option: str, fallback: Optional[bool] = None) -> bool:
        """获取布尔配置值"""
        return self.config.getboolean(section, option, fallback=fallback)


# 创建全局配置实例
config = Config()
