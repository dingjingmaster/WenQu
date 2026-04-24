# WenQu 脚本工具目录

此目录包含项目的所有可执行脚本。

## 📋 脚本列表

### start.sh - 启动服务器
启动 WenQu 服务器，包括：
- 检查虚拟环境
- 激活虚拟环境
- 检查配置文件
- 检查依赖服务（llama-server、PostgreSQL）
- 启动 FastAPI 服务器

**使用方式**:
```bash
bin/start.sh
```

### test.sh - 服务测试
测试服务器 API 接口是否正常工作：
- 健康检查接口
- 根路径访问
- API 文档访问

**使用方式**:
```bash
bin/test.sh
```

**注意**: 需要先启动服务器

### test_ui.sh - UI 测试
测试 UI 构建和集成是否完整：
- 检查前端构建文件
- 检查服务器静态文件
- 检查 Python 代码语法
- 检查 Python 依赖
- 检查 npm 依赖

**使用方式**:
```bash
bin/test_ui.sh
```

## 🔧 脚本特性

所有脚本都支持：
- ✅ 自动定位项目根目录（无论在哪个目录执行）
- ✅ 清晰的成功/失败提示
- ✅ 详细的错误信息
- ✅ 正确的退出码

## 📝 示例

```bash
# 从项目根目录执行
bin/test_ui.sh
bin/start.sh

# 从其他目录执行（使用绝对路径）
/data/code/WenQu/bin/test_ui.sh
/data/code/WenQu/bin/start.sh

# 测试服务器（需要先启动服务器）
bin/start.sh &  # 后台启动
sleep 2         # 等待启动
bin/test.sh     # 运行测试
```

## ⚠️ 注意事项

1. 所有脚本都应从项目根目录或通过绝对路径执行
2. 脚本会自动切换到项目根目录
3. 确保脚本有执行权限：`chmod +x bin/*.sh`
4. 不要将脚本文件放在项目根目录，统一放在 `bin/` 目录

---

*最后更新：2026-04-24*
