#!/bin/bash

# WenQu 服务测试脚本
# 该脚本应放在 bin/ 目录下

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# 项目根目录是 bin/ 的父目录
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 切换到项目根目录
cd "$PROJECT_ROOT"

SERVER_URL="http://localhost:8000"

echo "======================================"
echo "WenQu 服务测试"
echo "======================================"
echo ""

# 测试健康检查
echo "1. 测试健康检查接口..."
response=$(curl -s -w "\n%{http_code}" $SERVER_URL/health)
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" = "200" ]; then
    echo "✓ 健康检查通过：$body"
else
    echo "✗ 健康检查失败：HTTP $http_code"
fi
echo ""

# 测试根路径
echo "2. 测试根路径..."
response=$(curl -s -w "\n%{http_code}" $SERVER_URL/)
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" = "200" ]; then
    echo "✓ 根路径访问成功"
    echo "  响应：$body"
else
    echo "✗ 根路径访问失败：HTTP $http_code"
fi
echo ""

# 测试 API 文档
echo "3. 测试 API 文档..."
response=$(curl -s -o /dev/null -w "%{http_code}" $SERVER_URL/docs)

if [ "$response" = "200" ]; then
    echo "✓ API 文档可访问"
else
    echo "⚠ API 文档访问失败：HTTP $response"
fi
echo ""

echo "======================================"
echo "测试完成"
echo "======================================"
