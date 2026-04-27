import os
import asyncio
import uvicorn
from fastapi import FastAPI
from chainlit.utils import mount_chainlit
from src.config.WenQuConfig import getGlobalConfig

baseDir = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="WenQu", description="WenQu 本地 Agent 系统")

mount_chainlit(app=app, target=os.path.join(baseDir, "src/server/main.py"), path="/")


async  def main():
    serverConfig = uvicorn.Config(app=app, host="0.0.0.0", port=8000, loop="asyncio", lifespan="on", log_level="info", reload=True)
    server = uvicorn.Server(serverConfig)
    await server.serve()

if __name__ == "__main__":
    # 解析配置
    config = getGlobalConfig()
    if not config.loadConfig():
        print("parse config file error!")
        exit(-1)

    # 运行
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    exit(0)
