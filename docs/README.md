# WenQu 项目文档

> 本地 AI Agent 系统 - 智能需求分析与任务规划

## 📖 目录

- [项目概述](#项目概述)
- [需求说明](#需求说明)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
- [访问指南](#访问指南)
- [配置说明](#配置说明)
- [API 接口](#api-接口)
- [常见问题](#常见问题)

---

## 项目概述

WenQu 是一个本地 AI Agent 系统，用于处理用户的问题和请求。它基于大语言模型（通过 llama-server 提供），能够：

- 🤖 **智能分析**: 解析用户需求，自动拆分任务
- 📋 **生成 TODO**: 创建详细的任务列表
- ✅ **执行验证**: 逐步执行任务并验证结果
- 📚 **RAG 支持**: 基于文档的检索增强生成
- 💬 **交互界面**: 友好的 Web 界面

---

## 需求说明

### 工作流程

WenQu 的工作思路如下：

1. **解析用户请求**
   - 根据用户请求 + 提示词给到语言模型
   - 做进一步需求拆分
   - 明确用户描述的所有关键点

2. **生成 TODO 列表**
   - 基于分析结果确定实现步骤
   - 列成详细的 TODO 列表

3. **需求验证**
   - 检查 TODO 列表是否满足用户需求
   - 如不清晰则与用户沟通确认
   - 直到需求清晰为止

4. **任务执行**
   - 逐个实现 TODO 项
   - 每项完成后检查结果是否符合预期
   - 如不符合则调整，符合则继续下一项
   - 循环直到所有 TODO 项完成

5. **最终验证**
   - 检查实现结果是否满足用户需求
   - 如不满足则调整
   - 满足则输出结果给用户

### RAG 功能

系统扩展了 RAG（检索增强生成）功能：

1. **文档处理**
   - 支持网页、PDF、TXT、Markdown 格式
   - 使用 embedding 模型做语义分块
   - 将文档转换为向量表示

2. **向量存储**
   - 使用 PostgreSQL 向量数据库
   - 存储文档向量数据

3. **相似度搜索**
   - 基于用户请求做相似度搜索
   - 返回最相关的文档向量

4. **智能回复**
   - 基于检索结果生成最终回复
   - 使用语言模型生成准确答案

---

## 技术架构

### 整体架构

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

### 技术栈

- **UI 层**: Vue3 + ElementUI（编译为静态文件集成到服务器）
- **Agent 层**: Python 实现，智能需求分析与任务规划
- **RAG 层**: 
  - PostgreSQL 向量数据库
  - LlamaIndex 框架
  - llama-server 提供的 embedding 模型
- **推理层**: llama-server（提供 LLM 和 Embedding 能力）
- **服务器**: FastAPI + Uvicorn
- **包管理**: uv

### 项目结构

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
│   └── config.py       # 配置管理
├── docs/               # 文档目录
├── start.sh            # 启动脚本
├── test.sh             # 测试脚本
└── pyproject.toml      # 项目配置
```

---

## 快速开始

### 前置要求

已安装组件：
- ✅ PostgreSQL 数据库
- ✅ llama-server 模型服务
- ✅ llama-server 推理服务
- ✅ uv 包管理器

### 安装步骤

#### 1. 创建虚拟环境

```bash
cd /data/code/WenQu
uv venv
source .venv/bin/activate
```

#### 2. 安装依赖

```bash
uv pip install -e .
```

#### 3. 配置数据库

```bash
# 创建数据库
psql -U postgres -c 'CREATE DATABASE wenqu;'

# 初始化表结构
python src/rag/init_db.py
```

#### 4. 配置服务

编辑 `config/config.ini`：

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

#### 5. 启动服务

```bash
# 方法 1：使用启动脚本（推荐）
./start.sh

# 方法 2：手动启动
source .venv/bin/activate
uvicorn src.server.main:app --host 0.0.0.0 --port 8000
```

---

## 访问指南

### Web 界面

启动服务器后，在浏览器中访问：

#### 主页
```
http://localhost:8000
```

功能：
- 📝 输入你的需求
- 🚀 点击"分析需求"按钮
- 📋 查看 AI 生成的 TODO 列表

#### API 文档
```
http://localhost:8000/docs
```

Swagger UI 界面，可以测试所有 API 接口

#### 健康检查
```
http://localhost:8000/health
```

返回：`{"status": "healthy"}`

### 使用示例

#### 1. 需求分析

在主页文本框输入：
```
帮我创建一个简单的 Python Web 应用，需要实现用户登录功能
```

点击"🚀 分析需求"，系统会：
- 🎯 分析关键需求
- ❓ 指出不清晰点
- 📝 生成 TODO 列表

#### 2. 查看结果

结果以卡片形式展示：
- 关键需求列表
- 不清晰点列表
- TODO 任务列表

### 测试命令

```bash
# 测试首页
curl http://localhost:8000/

# 测试健康检查
curl http://localhost:8000/health

# 测试 API 文档
curl http://localhost:8000/docs
```

---

## 配置说明

### 配置文件位置

`config/config.ini`

### 配置项详解

#### [llm] - LLM 模型配置

```ini
[llm]
base_url = http://localhost:8080    # llama-server 服务地址
temperature = 0.7                   # 温度参数（0-1，越高越随机）
max_tokens = 1024                   # 最大生成 token 数
```

#### [embedding] - 嵌入模型配置

```ini
[embedding]
base_url = http://localhost:8080    # llama-server 服务地址
embed_dim = 768                     # 嵌入向量维度
```

#### [database] - 数据库配置

```ini
[database]
host = localhost                    # 数据库主机
port = 5432                         # 数据库端口
database = wenqu                    # 数据库名称
user = postgres                     # 数据库用户
password = postgres                 # 数据库密码
table_name = documents              # 向量表名
```

#### [server] - 服务器配置

```ini
[server]
host = 0.0.0.0                      # 监听地址
port = 8000                         # 服务端口
debug = false                       # 调试模式
```

#### [rag] - RAG 配置

```ini
[rag]
chunk_size = 1000                   # 文档分块大小
chunk_overlap = 200                 # 分块重叠大小
```

---

## API 接口

### 1. 分析需求

**接口**: `POST /api/analyze`

**请求**:
```json
{
  "user_input": "帮我创建一个 Python Web 应用",
  "context": ""
}
```

**响应**:
```json
{
  "key_points": ["关键点 1", "关键点 2"],
  "unclear_points": ["不清晰点 1"],
  "todos": [
    {"task": "任务 1", "priority": "high"},
    {"task": "任务 2", "priority": "medium"}
  ]
}
```

### 2. 执行任务

**接口**: `POST /api/execute`

**请求**:
```json
{
  "task_content": "创建 Hello World 应用",
  "context": "FastAPI 示例"
}
```

**响应**:
```json
{
  "result": "任务执行结果..."
}
```

### 3. 验证 TODO 列表

**接口**: `POST /api/validate`

**请求**:
```json
{
  "user_input": "用户需求",
  "todos": [{"task": "任务 1"}, {"task": "任务 2"}]
}
```

**响应**:
```json
{
  "validation_result": true
}
```

### 4. RAG 查询

**接口**: `POST /api/rag/query`

**请求**:
```json
{
  "query": "如何安装依赖？"
}
```

**响应**:
```json
{
  "answer": "基于文档的回答...",
  "sources": ["相关文档来源"]
}
```

---

## 常见问题

### 1. 页面空白

**原因**: 服务器未启动或启动失败

**解决**:
```bash
# 检查服务器是否运行
ps aux | grep uvicorn

# 重新启动服务器
./start.sh
```

### 2. 无法连接

**原因**: 端口被占用或防火墙阻止

**解决**:
```bash
# 检查端口占用
lsof -ti:8000 | xargs kill -9

# 修改配置文件使用其他端口
# 编辑 config/config.ini
[server]
port = 8001
```

### 3. llama-server 连接失败

**原因**: llama-server 未运行或配置错误

**解决**:
```bash
# 检查 llama-server 是否运行
curl http://localhost:8080/health

# 启动 llama-server
llama-server -m /path/to/model.gguf -c 4096
```

### 4. 数据库连接失败

**原因**: PostgreSQL 未运行或数据库未创建

**解决**:
```bash
# 检查 PostgreSQL 状态
sudo systemctl status postgresql

# 启动 PostgreSQL
sudo systemctl start postgresql

# 创建数据库
psql -U postgres -c 'CREATE DATABASE wenqu;'

# 初始化表结构
python src/rag/init_db.py
```

### 5. API 返回错误

**原因**: 参数错误或内部异常

**解决**:
- 检查请求参数格式
- 查看服务器日志获取详细错误信息
- 确保所有依赖服务正常运行

### 6. 模块导入错误

**原因**: 虚拟环境未激活或依赖未安装

**解决**:
```bash
# 激活虚拟环境
source .venv/bin/activate

# 重新安装依赖
uv pip install -e .
```

---

## 开发指南

### 代码风格

```bash
# 格式化代码
black src/

# 代码检查
flake8 src/
```

### 运行测试

```bash
# 使用测试脚本
./test.sh

# 或手动测试
curl http://localhost:8000/health
```

### 开发模式

```bash
# 开启调试模式（config/config.ini）
[server]
debug = true

# 重启服务（支持自动重载）
uvicorn src.server.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 错误处理

系统采用透明错误处理机制：

- ✅ 所有错误直接抛出给用户
- ✅ 不允许中断服务
- ✅ 详细的错误信息帮助定位问题

---

## 更新日志

### v0.1.0
- ✅ 基础 Agent 功能实现
- ✅ RAG 层集成
- ✅ Web 界面
- ✅ 配置管理
- ✅ 完整文档

---

## 许可证

MIT License

---

## 联系方式

如有问题，请通过以下方式联系：

- 📧 Email: dingjing@live.cn
- 📝 Issue: GitHub Issues

---

*最后更新：2026-04-24*
