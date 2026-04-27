import chainlit as cl
from src.agents.WenQuAgent import WenQuAgent

# 接口不兼容 ...
# cl.instrument_openai()

@cl.on_chat_start
async def web_root():
    await cl.Message(content='Welcome to use WenQu Local Agent.').send()

@cl.on_message
async def web_message (msg: cl.Message):
    agent = WenQuAgent(msg.id)
    question: str = str(msg.content)
    # out = cl.Message(content="")
    # res = agent.chat(question)
    # async for chunk in res:
    #     await out.stream_token(str(chunk))
    # await out.send()
    await cl.Message(content=agent.chatAsync(question)).send()

