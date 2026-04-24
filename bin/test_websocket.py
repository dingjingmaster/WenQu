#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebSocket 测试脚本
"""
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/agent"
    print(f"尝试连接到：{uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✓ WebSocket 连接成功!")
            
            # 接收连接成功消息
            response = await websocket.recv()
            print(f"收到服务器消息：{response}")
            
            # 发送测试消息
            test_msg = {"type": "test", "content": "Hello"}
            await websocket.send(json.dumps(test_msg))
            print(f"发送测试消息：{test_msg}")
            
            # 等待几秒看是否有响应
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=3.0)
                print(f"收到响应：{response}")
            except asyncio.TimeoutError:
                print("没有收到响应（这是正常的，因为我们发送的是测试消息）")
                
    except websockets.exceptions.ConnectionClosed as e:
        print(f"✗ WebSocket 连接关闭：{e}")
    except Exception as e:
        print(f"✗ 错误：{e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())
