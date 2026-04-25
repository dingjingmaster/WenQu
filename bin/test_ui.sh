#!/bin/bash

# WenQu UI 测试脚本
# 该脚本应放在 bin/ 目录下

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# 项目根目录是 bin/ 的父目录
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 切换到项目根目录
cd "$PROJECT_ROOT"

echo "======================================"
echo "WenQu UI 测试"
echo "======================================"
echo ""

# 检查前端文件
echo "检查前端文件..."
if [ -f "src/server/static/index.html" ]; then
    echo "✓ 前端 HTML 文件存在"
else
    echo "✗ 前端 HTML 文件不存在"
    exit 1
fi

if [ -f "src/server/static/assets/styles.css" ]; then
    echo "✓ CSS 样式文件存在"
else
    echo "✗ CSS 样式文件不存在"
    exit 1
fi

if [ -f "src/server/static/assets/app.js" ]; then
    echo "✓ JavaScript 文件存在"
else
    echo "✗ JavaScript 文件不存在"
    exit 1
fi

# 检查静态文件
echo "检查服务器静态文件..."
if [ -f "src/server/static/index.html" ]; then
    echo "✓ 服务器静态文件存在"
else
    echo "✗ 服务器静态文件不存在"
    exit 1
fi

# 检查 Python 语法
echo "检查 Python 服务器代码..."
if python -m py_compile src/server/main.py 2>/dev/null; then
    echo "✓ Python 代码语法正确"
else
    echo "✗ Python 代码语法错误"
    exit 1
fi

# 检查依赖
echo "检查 Python 依赖..."
if python -c "import fastapi; import uvicorn" 2>/dev/null; then
    echo "✓ Python 依赖已安装"
else
    echo "✗ Python 依赖未安装，请运行：uv pip install -e ."
    exit 1
fi



echo ""
echo "======================================"
echo "✓ 所有检查通过！"
echo "======================================"
echo ""
echo "启动服务器："
echo "  bin/start.sh"
echo ""
echo "访问地址："
echo "  http://localhost:8000"
echo ""
echo "API 文档："
echo "  http://localhost:8000/docs"
echo ""
