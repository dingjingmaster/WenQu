#!/usr/bin/env python
# -*- coding=utf-8 -*-
import chainlit as cl
import asyncio

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="")

    await msg.send()

    for i in range(10):
        await asyncio.sleep(0.3)
        await msg.stream_token(f"token-{i} ")

    await msg.update()
