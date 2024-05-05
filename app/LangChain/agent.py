#!/bin/env python
# -*- coding: utf-8

# import ollama
# from app.Utils.print import colorPrint
# from langchain.agents import AgentType
# from langchain.python import PythonREPL
# from langchain.chat_models import ChatOllama
# from langchain.agents import load_tools, initialize_agent
# from langchain.agents.agent_toolkits import create_python_agent
#
#
# class Agent(object):
#     def __init__(self):
#         # self.__llm = ollama.Client(host="http://127.0.0.1:11434")
#         self.__llm = ChatOllama(temperature=0)
#         self.__tools = load_tools(["llm-math", "wikipedia"], llm=self.__llm)
#         self.__agent = initialize_agent(
#             tools=self.__tools,
#             llm=self.__llm,
#             agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#             handle_parsing_errors=True,
#             verbose=True)
#     pass