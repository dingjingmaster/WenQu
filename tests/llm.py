#!/bin/env python
# -*- coding: utf-8 -*-

from app.llm.llm_llama import LLMOllama

if __name__ == "__main__":
    llm = LLMOllama()
    models = llm.getLocalModelList()
    print(models)

    llm.setModel("llama3:instruct")
    resp = llm.chat("你好!")
    print(resp['message']['content'])

    resp = llm.chat("Hello!")
    print(resp['message']['content'])
