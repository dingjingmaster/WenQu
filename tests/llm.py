#!/bin/env python
# -*- coding: utf-8 -*-

from app.LLMManager.ollama import LLMOllama

if __name__ == "__main__":
    llm = LLMOllama()
    models = llm.getLocalModelList()
    print(type(models))
    print(models)

    llm.setModel("llama3:instruct")
    resp = llm.chat("你好!")
    print(resp['message']['content'])

    resp = llm.chat("Hello!")
    print(resp['message']['content'])
