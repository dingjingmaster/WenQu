# WenQu 快速启动指南

## 最简启动步骤

### 1. 首次启动（完整流程）

```bash
# 进入项目目录
cd /data/code/WenQu

# 创建虚拟环境（仅首次）
uv venv

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖（仅首次）
uv pip install -e .

# 创建数据库（仅首次）
psql -U postgres -c 'CREATE DATABASE wenqu;'

# 初始化数据库表结构（仅首次）
python src/rag/init_db.py

# 启动服务
./start.sh
```

### 2. 日常启动（简化流程）

```bash
# 进入项目目录
cd /data/code/WenQu

# 直接启动（虚拟环境已存在）
./start.sh
```

## 启动脚本说明

`start.sh` 脚本会自动：
- ✅ 检查虚拟环境
- ✅ 激活虚拟环境
- ✅ 检查配置文件
- ✅ 检查 llama-server 服务状态
- ✅ 检查 PostgreSQL 数据库状态
- ✅ 启动 WenQu 服务器

## 访问服务

启动成功后，打开浏览器访问：

- 🌐 **Web 界面**: http://localhost:8000
- 📖 **API 文档**: http://localhost:8000/docs
- ❤️ **健康检查**: http://localhost:8000/health

## 测试服务

```bash
# 使用测试脚本
./test.sh

# 或手动测试
curl http://localhost:8000/health
```

## 常见问题

### 问题 1: 虚拟环境不存在

**错误**: `错误：虚拟环境不存在，请先运行：uv venv`

**解决**:
```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

### 问题 2: llama-server 未运行

**警告**: `⚠ 警告：llama-server 服务未运行`

**解决**: 启动 llama-server
```bash
llama-server -m /path/to/your/model.gguf -c 4096
```

### 问题 3: 数据库未初始化

**错误**: 数据库连接成功但查询失败

**解决**:
```bash
# 创建数据库
psql -U postgres -c 'CREATE DATABASE wenqu;'

# 初始化表结构
python src/rag/init_db.py
```

### 问题 4: 端口被占用

**错误**: `Address already in use`

**解决**:
```bash
# 方法 1: 停止占用端口的进程
lsof -ti:8000 | xargs kill -9

# 方法 2: 修改配置文件使用其他端口
# 编辑 config/config.ini
[server]
port = 8001
```

## 停止服务

按 `Ctrl+C` 停止服务器

## 开发模式

需要代码自动重载：

```bash
# 编辑 config/config.ini
[server]
debug = true

# 重启服务
./start.sh
```

## 完整启动流程图

```
┌─────────────────┐
│  运行 ./start.sh │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 检查虚拟环境    │─── 不存在 ──▶ 报错退出
└────────┬────────┘
         │ 存在
         ▼
┌─────────────────┐
│ 激活虚拟环境    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 检查配置文件    │─── 不存在 ──▶ 报错退出
└────────┬────────┘
         │ 存在
         ▼
┌─────────────────┐
│ 检查 llama-server│─── 未运行 ──▶ 显示警告
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 检查 PostgreSQL  │─── 未运行 ──▶ 显示警告
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 启动服务器      │
│ 0.0.0.0:8000    │
└─────────────────┘
```

## 下一步

服务启动后，你可以：

1. 访问 API 文档了解所有接口
2. 测试 Agent 功能
3. 上传文档到 RAG 系统
4. 开发新功能

祝你使用愉快！🎉
