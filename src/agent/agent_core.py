import requests
import json
from pydantic import BaseModel, Field
from typing import List, Optional
from src.config import config

# 定义 TODO 项的数据结构
class TodoItem(BaseModel):
    id: str = Field(description="任务 ID")
    content: str = Field(description="任务内容")
    status: str = Field(description="任务状态：pending, in_progress, completed")
    priority: str = Field(description="任务优先级：high, medium, low")

# 定义 TODO 列表的数据结构
class TodoList(BaseModel):
    todos: List[TodoItem] = Field(description="TODO 列表")

# 定义用户需求分析结果
class RequirementAnalysis(BaseModel):
    key_points: List[str] = Field(description="用户需求的关键点")
    unclear_points: List[str] = Field(description="不清晰需要进一步确认的点")
    todos: List[TodoItem] = Field(description="实现用户需求需要的 TODO 列表")

class LlamaServerClient:
    """llama-server 客户端"""
    
    def __init__(self):
        self.base_url = config.llm_base_url
        self.temperature = config.llm_temperature
        self.max_tokens = config.llm_max_tokens
        self.chat_endpoint = f"{self.base_url}/chat/completions"
    
    def chat(self, messages: list, temperature: Optional[float] = None, max_tokens: Optional[int] = None) -> str:
        """
        发送聊天请求到 llama-server
        
        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "消息内容"}]
            temperature: 温度参数
            max_tokens: 最大 token 数
            
        Returns:
            模型回复内容
        """
        payload = {
            "messages": messages,
            "temperature": temperature or self.temperature,
            "max_tokens": max_tokens or self.max_tokens
        }
        
        response = requests.post(self.chat_endpoint, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    def chat_with_json_output(self, messages: list, output_schema: dict) -> dict:
        """
        发送聊天请求并要求 JSON 格式输出
        
        Args:
            messages: 消息列表
            output_schema: 期望的 JSON 格式 schema
            
        Returns:
            解析后的 JSON 对象
        """
        # 添加系统提示要求 JSON 输出
        system_message = {
            "role": "system",
            "content": f"请严格按照以下 JSON Schema 格式输出：\n{json.dumps(output_schema, ensure_ascii=False)}\n\n只输出 JSON，不要有其他内容。"
        }
        messages_with_system = [system_message] + messages
        
        response_text = self.chat(messages_with_system)
        
        # 尝试解析 JSON
        try:
            # 清理可能的 markdown 格式
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            raise Exception(f"JSON 解析失败：{str(e)}，原始响应：{response_text}")

class WenQuAgent:
    """WenQu Agent 核心类，负责用户需求分析、任务规划和执行"""
    
    def __init__(self):
        self.client = LlamaServerClient()
    
    def analyze_requirement(self, user_input: str) -> RequirementAnalysis:
        """分析用户需求，生成 TODO 列表"""
        messages = [
            {
                "role": "user",
                "content": f"""请分析以下用户需求：
{user_input}

请完成以下任务：
1. 列出所有关键点
2. 识别是否有不清晰需要进一步确认的地方
3. 生成实现该需求需要的 TODO 列表

请以 JSON 格式输出，格式如下：
{{
    "key_points": ["关键点 1", "关键点 2", ...],
    "unclear_points": ["不清晰点 1", ...],
    "todos": [
        {{"id": "1", "content": "任务内容", "status": "pending", "priority": "high"}},
        ...
    ]
}}"""
            }
        ]
        
        output_schema = {
            "type": "object",
            "properties": {
                "key_points": {"type": "array", "items": {"type": "string"}},
                "unclear_points": {"type": "array", "items": {"type": "string"}},
                "todos": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "content": {"type": "string"},
                            "status": {"type": "string", "enum": ["pending", "in_progress", "completed"]},
                            "priority": {"type": "string", "enum": ["high", "medium", "low"]}
                        },
                        "required": ["id", "content", "status", "priority"]
                    }
                }
            },
            "required": ["key_points", "unclear_points", "todos"]
        }
        
        result = self.client.chat_with_json_output(messages, output_schema)
        
        # 转换为 Pydantic 模型
        todos = [TodoItem(**todo) for todo in result.get("todos", [])]
        return RequirementAnalysis(
            key_points=result.get("key_points", []),
            unclear_points=result.get("unclear_points", []),
            todos=todos
        )
    
    def validate_todos(self, user_input: str, todos: List[TodoItem]) -> str:
        """验证 TODO 列表是否满足用户需求"""
        todos_str = json.dumps([todo.model_dump() for todo in todos], ensure_ascii=False, indent=2)
        
        messages = [
            {
                "role": "user",
                "content": f"""用户需求：{user_input}
TODO 列表：
{todos_str}

请判断该 TODO 列表是否能满足用户需求，如果不能，请说明原因。"""
            }
        ]
        
        return self.client.chat(messages)
    
    def execute_task(self, task_content: str, context: str = "") -> str:
        """执行具体任务"""
        messages = [
            {
                "role": "user",
                "content": f"""请执行以下任务：
{task_content}

当前上下文：{context}

请输出执行结果。"""
            }
        ]
        
        return self.client.chat(messages)
    
    def run(self, user_input: str) -> dict:
        """运行完整的 Agent 流程"""
        # 1. 分析用户需求
        print("正在分析用户需求...")
        analysis = self.analyze_requirement(user_input)
        
        # 2. 检查是否有不清晰的点
        if analysis.unclear_points:
            print("发现以下不清晰的点：")
            for point in analysis.unclear_points:
                print(f"  - {point}")
        
        # 3. 输出 TODO 列表
        print(f"生成 TODO 列表，共 {len(analysis.todos)} 项任务")
        
        return {
            "key_points": analysis.key_points,
            "unclear_points": analysis.unclear_points,
            "todos": [todo.model_dump() for todo in analysis.todos]
        }

# 测试函数
if __name__ == "__main__":
    agent = WenQuAgent()
    result = agent.run("帮我创建一个简单的 Python Web 应用")
    print("\n分析结果：")
    print(json.dumps(result, ensure_ascii=False, indent=2))
