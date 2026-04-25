# WenQu - 本地 AI Agent 系统

> 基于 llama-server 实现的本地 AI Agent 系统，提供需求分析、任务规划和执行能力

📖 **完整文档**: [docs/README.md](docs/README.md)

## 特性

- 🤖 **智能 Agent**: 分析用户需求，生成 TODO 列表，执行任务
- 📚 **RAG 支持**: 基于文档的检索增强生成，使用 llama-server embedding
- 🗄️ **持久化存储**: PostgreSQL 向量数据库存储文档和上下文
- 🔧 **灵活配置**: 统一的配置文件管理所有参数
- 🚀 **简单易用**: 一键启动脚本，快速部署
- ✨ **炫酷 UI**: 粒子背景、交互动画、纯 HTML/CSS/JS 实现（零依赖）
- 💭 **思考可视化**: 实时显示模型思考过程

## 架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   UI/API    │────▶│   Agent     │────▶│  llama-     │
│   (FastAPI) │     │   (Python)  │     │  server     │
└─────────────┘     └─────────────┘     └─────────────┘
                           │                    │
                           ▼                    ▼
                    ┌─────────────┐     ┌─────────────┐
                    │   RAG       │     │  LLM &      │
                    │   Service   │────▶│  Embedding  │
                    └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ PostgreSQL  │
                    │ (Vector DB) │
                    └─────────────┘
```

## 快速开始

### 1. 前置要求

- **llama-server**: 运行大模型（支持 `/chat/completions` 和 `/embedding` 接口）
- **PostgreSQL**: 向量数据库
- **Python 3.10+**: 运行环境
- **uv**: 包管理器

### 2. 安装

```bash
# 克隆项目
cd /data/code/WenQu

# 创建虚拟环境
uv venv

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
uv pip install -e .
```

### 3. 配置

编辑 `config/config.ini` 文件：

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

### 4. 初始化数据库

```bash
# 创建数据库
psql -U postgres -c 'CREATE DATABASE wenqu;'

# 初始化表结构
python src/rag/init_db.py
```

### 5. 启动服务

```bash
# 方法一：使用启动脚本（推荐）
./start.sh

# 方法二：手动启动
python src/server/main.py

# 方法三：使用 uvicorn
uvicorn src.server.main:app --host 0.0.0.0 --port 8000
```

### 6. 访问服务

- **Web 界面**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 使用示例

### API 调用

```bash
# 分析用户需求
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"user_input": "帮我创建一个简单的 Python Web 应用"}'

# 执行任务
curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"task_content": "创建 Hello World 应用", "context": "FastAPI 示例"}'
```

### Python 调用

```python
from src.agent.agent_core import WenQuAgent
from src.rag.rag_service import rag_service

# 创建 Agent
agent = WenQuAgent()

# 分析需求
result = agent.run("帮我创建一个简单的 Python Web 应用")
print(result)

# 使用 RAG 服务
embedding = rag_service.get_embedding("示例文本")
similarity = rag_service.cosine_similarity(embedding1, embedding2)
response = rag_service.generate_response("问题", "上下文")
```

## 项目结构

```
WenQu/
├── config/              # 配置文件目录
│   ├── config.ini      # 主配置文件
│   └── README.md       # 配置说明
├── src/                # 源代码目录
│   ├── agent/          # Agent 层
│   ├── rag/            # RAG 层
│   ├── inference/      # 推理层
│   ├── server/         # 服务器
│   │   ├── static/     # UI 静态文件
│   │   │   ├── assets/ # CSS 和 JavaScript 文件
│   │   │   │   ├── styles.css
│   │   │   │   ├── app.js
│   │   │   │   ├── particles.min.js  # 粒子背景动画库
│   │   │   │   └── anime.min.js      # 高级动画库
│   │   │   └── index.html
│   │   ├── uploads/    # 上传文件目录
│   │   └── main.py     # FastAPI 服务器
│   └── config.py       # 配置管理
├── docs/               # 文档目录
├── bin/                # 脚本工具目录
│   ├── start.sh        # 启动脚本
│   ├── test.sh         # 服务测试脚本
│   └── test_ui.sh      # UI 测试脚本
├── tests/              # 测试目录
├── start.sh            # 启动脚本
├── test.sh             # 测试脚本
├── RUNNING.md          # 运行说明
└── pyproject.toml      # 项目配置
```

## 核心模块

### Agent 层 (`src/agent/`)
- 用户需求分析
- TODO 列表生成
- 任务执行和验证

### RAG 层 (`src/rag/`)
- 文档处理
- 向量嵌入（使用 llama-server）
- 相似度检索
- 基于上下文的回复生成

### 推理层 (`src/inference/`)
- llama-server 客户端
- 文本生成
- 聊天补全

### 服务器 (`src/server/`)
- FastAPI Web 服务
- RESTful API
- WebSocket 实时通信
- 错误处理
- 静态文件服务（HTML/CSS/JS）

### UI 层 (`src/server/static/`)
- 纯 HTML5/CSS3/JavaScript 实现
- 粒子背景动画（particles.js）
- 高级动画引擎（anime.js）
- Google 风格界面设计
- 响应式布局
- 零依赖（不使用 Vue/React/npm）

## 配置说明

详细配置说明见 [config/README.md](config/README.md)

主要配置项：
- **LLM 配置**: 模型地址、温度、最大 token 数
- **Embedding 配置**: 嵌入服务地址、向量维度
- **数据库配置**: PostgreSQL 连接信息
- **服务器配置**: 监听地址、端口、调试模式

## 开发

### 运行测试

```bash
# 运行测试脚本
./test.sh

# 或手动测试
curl http://localhost:8000/health
```

### 代码风格

```bash
# 格式化代码
black src/

# 代码检查
flake8 src/
```

## 常见问题

### llama-server 连接失败
- 确保 llama-server 已启动：`curl http://localhost:8080/health`
- 检查配置文件中的 `base_url` 是否正确

### 数据库连接失败
- 确保 PostgreSQL 服务已启动
- 检查数据库 `wenqu` 是否已创建

### 模块导入错误
```bash
# 确保已激活虚拟环境
source .venv/bin/activate

# 重新安装依赖
uv pip install -e .
```

## 技术栈

- **后端**: Python 3.10+, FastAPI
- **数据库**: PostgreSQL (pgvector)
- **大模型**: llama-server (llama.cpp)
- **包管理**: uv
- **配置管理**: configparser

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 致谢

- [llama.cpp](https://github.com/ggerganov/llama.cpp) - 高效的 LLM 推理框架
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Python Web 框架
- [PostgreSQL](https://www.postgresql.org/) - 强大的开源数据库
