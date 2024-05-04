# AI助手

> 借助开源大模型实现自己的本地AI助手

## 环境搭建

### 安装ollama

ollama 用来拉取和运行开源大模型

```shell
pacman -S ollama
```

> 包管理器里没有，则去官网手动下载：[https://ollama.com/](https://ollama.com/)

### 安装poetry

peotry 用来管理python项目依赖

```shell
pacman -S ollama
```

### 使用ollama拉取大模型

#### llama3

```shell
ollama pull llama3:instruct
```

> 此项目使用的是 "llama3:instruct"

### 运行本地客户端

```shell
git pull https://github.com/dingjingmaster/WenQu.git
cd WenQu
poetry run ./main.py
```
