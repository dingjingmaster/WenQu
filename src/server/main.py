import chainlit as cl
from src.agents.WenQuAgent import WenQuAgent

# 接口不兼容 ...
# cl.instrument_openai()

@cl.on_chat_start
async def web_root():
    await cl.Message(content='欢迎使用 WenQu 本地大语言模型.').send()

@cl.on_message
async def web_message (msg: cl.Message):
    sessionId = cl.context.session.id
    agent = WenQuAgent(sessionId)
    question: str = str(msg.content)

    # 同步
    # await cl.Message(content=agent.chatAsync(question)).send()

    # 异步
    out = cl.Message(content="")
    res = agent.chatSync(question)
    async for chunk in res:
        await out.stream_token(str(chunk))
    await out.send()

