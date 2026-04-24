from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os
from typing import List, Optional
import uvicorn
import json
import asyncio
from datetime import datetime

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

# WebSocket 连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

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
    return {"message": "欢迎使用 WenQu API", "version": "0.1.0"}

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
async def execute_task(task_content: str, context: str = ""):
    """
    执行具体任务
    
    Args:
        task_content: 任务内容
        context: 上下文信息
        
    Returns:
        执行结果
    """
    try:
        result = agent.execute_task(task_content, context or "")
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

@app.websocket("/ws/agent")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket 连接端点，用于实时推送 Agent 执行状态
    """
    await manager.connect(websocket)
    try:
        # 发送连接成功消息
        await websocket.send_json({
            "type": "connected",
            "message": "WebSocket 连接成功",
            "timestamp": datetime.now().isoformat()
        })
        
        # 保持连接
        while True:
            try:
                # 接收客户端消息（如果需要）
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30)
                # 可以处理客户端发来的消息
            except asyncio.TimeoutError:
                # 发送心跳
                await websocket.send_json({
                    "type": "heartbeat",
                    "timestamp": datetime.now().isoformat()
                })
            except WebSocketDisconnect:
                break
    except Exception as e:
        pass
    finally:
        manager.disconnect(websocket)

@app.post("/api/agent/execute")
async def agent_execute(
    query: str = Form(...),
    files: Optional[List[UploadFile]] = File(None)
):
    """
    Agent 执行接口，支持文件上传
    
    Args:
        query: 用户查询
        files: 上传的文件列表
        
    Returns:
        执行结果
    """
    try:
        # 发送开始消息
        await manager.broadcast({
            "type": "log",
            "content": f"开始处理查询：{query[:50]}...",
            "timestamp": datetime.now().isoformat()
        })
        
        # 处理上传的文件
        file_paths = []
        if files:
            upload_dir = os.path.join(os.path.dirname(__file__), "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            
            for file in files:
                if file.filename:
                    file_path = os.path.join(upload_dir, file.filename)
                    with open(file_path, "wb") as f:
                        content = await file.read()
                        f.write(content)
                    file_paths.append(file_path)
            
            await manager.broadcast({
                "type": "log",
                "content": f"已上传 {len(file_paths)} 个文件",
                "timestamp": datetime.now().isoformat()
            })
        
        # 执行 Agent 任务
        result = agent.run(query)
        
        # 发送结果
        await manager.broadcast({
            "type": "result",
            "content": json.dumps(result, ensure_ascii=False, indent=2),
            "timestamp": datetime.now().isoformat()
        })
        
        return {"success": True, "message": "任务已提交"}
    except Exception as e:
        await manager.broadcast({
            "type": "error",
            "content": str(e),
            "timestamp": datetime.now().isoformat()
        })
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
