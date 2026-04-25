#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试完整的 WebSocket + Agent 执行流程
"""
import asyncio
import websockets
import requests
import json

async def receive_messages(websocket, duration=10):
    """接收 WebSocket 消息"""
    try:
        end_time = asyncio.get_event_loop().time() + duration
        while asyncio.get_event_loop().time() < end_time:
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                data = json.loads(message)
                print(f"\n收到 WebSocket 消息:")
                print(f"  类型：{data.get('type')}")
                print(f"  内容：{str(data.get('content', ''))[:200]}")
            except asyncio.TimeoutError:
                continue
    except Exception as e:
        print(f"接收消息结束：{e}")

async def test_full_flow():
    uri = "ws://localhost:8000/ws/agent"
    print(f"1. 连接到 WebSocket: {uri}")
    
    async with websockets.connect(uri) as websocket:
        print("✓ WebSocket 连接成功!")
        
        # 接收连接成功消息
        response = await websocket.recv()
        print(f"收到：{response}")
        
        # 启动消息接收任务
        receiver_task = asyncio.create_task(receive_messages(websocket, duration=15))
        
        # 等待 1 秒确保连接稳定
        await asyncio.sleep(1)
        
        print("\n2. 发送 HTTP 请求执行 Agent 任务...")
        # 发送 HTTP 请求执行任务
        response = requests.post(
            'http://localhost:8000/api/agent/execute',
            data={'query': '请帮我分析 Python 是什么'},
            timeout=30
        )
        
        print(f"HTTP 响应状态：{response.status_code}")
        print(f"HTTP 响应数据：{response.json()}")
        
        # 继续接收 WebSocket 消息
        print("\n3. 等待 WebSocket 消息...")
        await receiver_task
        
        print("\n✓ 测试完成!")

if __name__ == "__main__":
    asyncio.run(test_full_flow())
