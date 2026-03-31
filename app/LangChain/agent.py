#!/bin/env python
# -*- coding: utf-8

class LlamaDeepAgent:
    def __init__(self, llm, tools):
        self._llm = llm
        self._tools = tools

    def invoke(self, query: str):
        prompt = f"""你是一个AI代理，可以使用工具来回答问题。

请严格遵循以下规则：

1. 如果需要使用工具，使用格式：
Thought: ...
Action: 工具名
Action Input: ...
Observation: 工具返回结果
...（可以重复多次）
Final Answer: 最终答案

2. 如果不需要使用工具，直接输出：
Thought: ...
Final Answer: 最终答案

⚠️ 注意：
- 不要在不需要工具时输出 Action
- 不要编造工具调用

Question: {query}
        """
        return self._llm.invoke(prompt)