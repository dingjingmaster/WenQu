from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os
from typing import List, Optional
import uvicorn

# 导入配置
from src.config import config

# 导入 Agent 和 RAG 模块
from src.agent.agent_core import WenQuAgent, TodoItem
from src.rag.rag_service import rag_service

# 创建 FastAPI 应用
app = FastAPI(title="WenQu API", description="WenQu 本地 Agent 系统 API")

# 设置静态文件目录
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

# 初始化 Agent
agent = WenQuAgent()

# 请求模型
class UserRequest(BaseModel):
    user_input: str
    context: Optional[str] = ""

# 文件上传响应模型
class UploadResponse(BaseModel):
    message: str
    filename: str

# 分析响应模型
class AnalysisResponse(BaseModel):
    key_points: List[str]
    unclear_points: List[str]
    todos: List[dict]

# API 路由
@app.get("/")
async def root():
    """根路径，返回欢迎页面"""
    index_path = os.path.join(static_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "欢迎使用 WenQu API", "version": "0.1.0", "docs": "/docs"}

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_request(request: UserRequest):
    """
    分析用户需求，生成 TODO 列表
    
    Args:
        request: 用户请求
        
    Returns:
        分析结果，包括关键点、不清晰点和 TODO 列表
    """
    try:
        result = agent.run(request.user_input)
        return AnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/execute")
async def execute_task(task_content: str, context: Optional[str] = ""):
    """
    执行具体任务
    
    Args:
        task_content: 任务内容
        context: 上下文信息
        
    Returns:
        执行结果
    """
    try:
        result = agent.execute_task(task_content, context)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/validate")
async def validate_todos(user_input: str, todos: List[dict]):
    """
    验证 TODO 列表是否满足用户需求
    
    Args:
        user_input: 用户需求
        todos: TODO 列表
        
    Returns:
        验证结果
    """
    try:
        todo_items = [TodoItem(**todo) for todo in todos]
        result = agent.validate_todos(user_input, todo_items)
        return {"validation_result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/documents/upload")
async def upload_document(file_path: str):
    """
    上传文档并处理
    
    Args:
        file_path: 文件路径
        
    Returns:
        上传结果
    """
    try:
        # 这里简化处理，实际需要实现文件上传逻辑
        return UploadResponse(
            message="文档上传成功",
            filename=os.path.basename(file_path)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rag/query")
async def rag_query(query: str):
    """
    RAG 查询接口
    
    Args:
        query: 查询内容
        
    Returns:
        查询结果
    """
    try:
        # 这里需要先初始化索引，实际使用时应该从数据库加载
        return {"message": "RAG 查询功能暂未完全实现"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 错误处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

# 启动服务器
def main():
    """主函数，启动服务器"""
    uvicorn.run(
        app, 
        host=config.server_host, 
        port=config.server_port,
        reload=config.server_debug
    )

if __name__ == "__main__":
    main()
