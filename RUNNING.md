# WenQu 运行说明

## 前置要求

### 1. llama-server 服务
确保已安装并运行 llama-server，并且加载了合适的模型：

```bash
# 示例：启动 llama-server
llama-server -m /path/to/your/model.gguf -c 4096 --host 0.0.0.0 --port 8080
```

**要求：**
- llama-server 需要支持 `/chat/completions` 和 `/embedding` 接口
- 建议使用最新的 llama.cpp 版本

### 2. PostgreSQL 数据库
确保已安装并运行 PostgreSQL 数据库：

```bash
# 检查 PostgreSQL 状态
sudo systemctl status postgresql

# 启动 PostgreSQL
sudo systemctl start postgresql
```

### 3. Python 环境
确保已安装 uv 包管理器：

```bash
# 检查 uv 是否已安装
uv --version
```

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境
source .venv/bin/activate

# 安装项目依赖
uv pip install -e .
```

### 2. 配置数据库

```bash
# 创建数据库（如果不存在）
psql -U postgres -c 'CREATE DATABASE wenqu;'

# 初始化表结构
python src/rag/init_db.py
```

### 3. 配置文件

编辑 `config/config.ini` 文件，根据你的环境修改配置：

```ini
[llm]
base_url = http://localhost:8080
temperature = 0.7
max_tokens = 1024

[embedding]
base_url = http://localhost:8080
embed_dim = 768

[database]
host = localhost
port = 5432
database = wenqu
user = postgres
password = postgres

[server]
host = 0.0.0.0
port = 8000
debug = false
```

### 4. 启动服务

#### 方法一：使用启动脚本（推荐）

```bash
# 给脚本添加执行权限
chmod +x start.sh

# 运行启动脚本
./start.sh
```

#### 方法二：手动启动

```bash
# 激活虚拟环境
source .venv/bin/activate

# 启动服务器
python src/server/main.py
```

或者使用 uvicorn 直接启动：

```bash
source .venv/bin/activate
uvicorn src.server.main:app --host 0.0.0.0 --port 8000
```

## 访问服务

启动成功后，可以通过以下方式访问：

- **Web 界面**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs (Swagger UI)
- **健康检查**: http://localhost:8000/health

## API 使用示例

### 1. 分析用户需求

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "帮我创建一个简单的 Python Web 应用"
  }'
```

### 2. 执行任务

```bash
curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task_content": "创建一个 Hello World 的 FastAPI 应用",
    "context": "用户需要一个简单的示例"
  }'
```

### 3. RAG 查询

```bash
curl -X POST http://localhost:8000/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "如何安装依赖？"
  }'
```

## 常见问题

### 1. llama-server 连接失败

**错误信息**: `Connection refused` 或 `Connection error`

**解决方案**:
- 确保 llama-server 已启动：`curl http://localhost:8080/health`
- 检查配置文件中的 `base_url` 是否正确
- 确保端口 8080 未被占用

### 2. 数据库连接失败

**错误信息**: `could not connect to server`

**解决方案**:
- 确保 PostgreSQL 服务已启动
- 检查配置文件中的数据库连接信息
- 确认数据库 `wenqu` 已创建

### 3. 模块导入错误

**错误信息**: `ModuleNotFoundError`

**解决方案**:
```bash
# 确保已激活虚拟环境
source .venv/bin/activate

# 重新安装依赖
uv pip install -e .
```

## 开发模式

如果需要开启调试模式自动重载：

```bash
# 修改 config/config.ini
[server]
debug = true

# 或者使用命令行参数
uvicorn src.server.main:app --host 0.0.0.0 --port 8000 --reload
```

## 停止服务

```bash
# 按 Ctrl+C 停止服务器
```

## 查看日志

服务器日志会直接输出到控制台，包括：
- HTTP 请求日志
- 错误信息
- 调试信息（debug 模式下）

## 性能优化建议

1. **llama-server 配置**:
   - 使用 GPU 加速（如果可用）
   - 调整 context size (`-c` 参数)
   - 使用量化模型减少内存占用

2. **数据库优化**:
   - 为向量列创建索引
   - 定期清理无用数据

3. **服务器配置**:
   - 生产环境使用 gunicorn + uvicorn workers
   - 配置合适的 worker 数量

## 下一步

项目启动后，你可以：
1. 访问 API 文档了解所有可用接口
2. 测试 Agent 功能，分析用户需求
3. 上传文档到 RAG 系统
4. 根据需求扩展功能
