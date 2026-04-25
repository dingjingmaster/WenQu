#!/bin/bash

# WenQu 项目启动脚本
# 该脚本应放在 bin/ 目录下

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# 项目根目录是 bin/ 的父目录
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "======================================"
echo "WenQu 本地 Agent 系统"
echo "======================================"
echo ""

# 切换到项目根目录
cd "$PROJECT_ROOT"

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "错误：虚拟环境不存在，请先运行：uv venv"
    exit 1
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source .venv/bin/activate

# 检查配置文件
if [ ! -f "config/config.ini" ]; then
    echo "错误：配置文件 config/config.ini 不存在"
    exit 1
fi

echo "配置文件检查通过"
echo ""

# 检查 llama-server 是否运行
echo "检查 llama-server 服务状态..."
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "✓ llama-server 服务运行正常"
else
    echo "⚠ 警告：llama-server 服务未运行，请确保已启动 llama-server"
    echo "  启动命令示例：llama-server -m /path/to/model.gguf -c 4096"
fi
echo ""

# 检查 PostgreSQL 是否运行
echo "检查 PostgreSQL 数据库状态..."
if psql -U postgres -c '\q' > /dev/null 2>&1; then
    echo "✓ PostgreSQL 数据库连接正常"
else
    echo "⚠ 警告：PostgreSQL 数据库未运行或无法连接"
fi
echo ""

# 启动服务器
echo "启动 WenQu 服务器..."
echo "服务器地址：http://localhost:8000"
echo "API 文档：http://localhost:8000/docs"
echo ""

# 使用 uvicorn 启动，支持自动重载和更好的性能
uvicorn src.server.main:app --host 0.0.0.0 --port 8000
