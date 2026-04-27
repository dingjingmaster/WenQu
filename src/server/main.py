import chainlit as cl


@cl.on_chat_start
async def web_root():
    await cl.Message(content='Welcome to use WenQu Local Agent.').send()

@cl.on_message
async def web_message (message: cl.Message):
    print(message.content)
    print(message.id)
    await message.send()

