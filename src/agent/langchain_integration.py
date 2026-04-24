from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from typing import List

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

# 初始化 Ollama 模型
llm = ChatOllama(
    model="qwen",
    base_url="http://localhost:11434"
)

# 用户需求分析提示词
analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的需求分析助手，负责分析用户需求并生成 TODO 列表。"),
    ("human", "请分析以下用户需求：\n{user_input}\n\n"
              "请列出所有关键点，并识别是否有不清晰需要进一步确认的地方。\n"
              "然后生成实现该需求需要的 TODO 列表。")
])

# 创建分析链
analysis_chain = analysis_prompt | llm.with_structured_output(RequirementAnalysis)

# TODO 列表验证提示词
validation_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的任务规划助手，负责验证 TODO 列表是否满足用户需求。"),
    ("human", "用户需求：{user_input}\n"
              "TODO 列表：{todos}\n\n"
              "请判断该 TODO 列表是否能满足用户需求，如果不能，请说明原因。")
])

# 创建验证链
validation_chain = validation_prompt | llm
