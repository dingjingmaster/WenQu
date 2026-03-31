# AI助手

> 借助开源大模型实现自己的本地AI助手

## 环境搭建

- [x] llama-cpp 运行大模型
- [x] PostgreSQL 为模型提供持久记忆(目前仅保存上下文...)
- [x] 增加Qt界面支持

## llama-cpp-python支持 AMD GPU

```
# 1. 生成.venv
poetry env activate

# 2. 激活虚拟环境
python -m venv .venv
. .venv/bin/activate

# 3. 重新编译 llama-cpp 支持 amd GPU, 默认不支持 ....
CMAKE_ARGS="-DGGML_HIPBLAS=on -DGGML_HIP=ON" pip install llama-cpp-python --no-binary llama-cpp-python --upgrade --force-reinstall --no-cache-dir -v

# 4. 取消激活虚拟环境
deactive
```
