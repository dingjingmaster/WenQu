# WenQu 配置说明

## 配置文件位置

配置文件位于项目根目录的 `config/config.ini`

## 配置项说明

### [llm]
LLM 模型配置，所有大模型相关能力都通过 llama-server 提供

- `base_url`: llama-server 服务地址，默认 `http://localhost:8080`
- `temperature`: 温度参数，控制生成随机性，默认 `0.7`
- `max_tokens`: 最大生成 token 数，默认 `1024`

### [embedding]
嵌入模型配置，使用 llama-server 提供的 embedding 能力

- `base_url`: llama-server 服务地址，默认 `http://localhost:8080`
- `embed_dim`: 嵌入向量维度，默认 `768`

### [database]
PostgreSQL 数据库配置

- `host`: 数据库主机，默认 `localhost`
- `port`: 数据库端口，默认 `5432`
- `database`: 数据库名称，默认 `wenqu`
- `user`: 数据库用户，默认 `postgres`
- `password`: 数据库密码，默认 `postgres`
- `table_name`: 向量表名，默认 `documents`

### [server]
服务器配置

- `host`: 服务器监听地址，默认 `0.0.0.0`
- `port`: 服务器端口，默认 `8000`
- `debug`: 是否开启调试模式，默认 `false`

### [rag]
RAG 配置

- `chunk_size`: 文档分块大小，默认 `1000`
- `chunk_overlap`: 分块重叠大小，默认 `200`

## 使用说明

1. 修改 `config/config.ini` 配置文件
2. 所有配置会自动被代码读取使用
3. 无需修改代码即可切换不同的服务地址和参数

## 注意事项

- 所有大模型相关能力（LLM、Embedding）都通过 llama-server 提供
- 无需配置 ollama、HuggingFace 等其他服务
- 确保 llama-server 服务已启动并可访问
