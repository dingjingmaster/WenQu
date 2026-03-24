import sys
from typing import Any


import os
import langchain

from app.Utils.print import colorPrint
from langchain_openai import ChatOpenAI
from deepagents import create_deep_agent
from langchain.messages import AIMessage, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

# from app.LangChain.tools import *


class LLMOpenAI(object):
    def __init__(self):
        self._lastResponse = []
        os.environ["OPENAI_API_KEY"] = "sk-local"
        langchain.debug = False
        agentTools = [
            # tool_current_date,
            # tool_current_date_time,
        ]
        tools = []
        self.__agentTools = tools + agentTools
        self._client = ChatOpenAI(model="localLLM", base_url="http://127.0.0.1:9999/v1", max_retries=60, timeout=120, streaming=True)

    def chat(self, question: str):
        resp = self._client.invoke(input=question)
        return resp.content

    def agent(self, question:str) -> str:
        ret = "您的提问超出了我的能力范围."
        agent = create_deep_agent(model=self._client, tools=self.__agentTools)
        try:
            message = []
            if not self._lastResponse is None:
                message += self._lastResponse
            message += [
                HumanMessage(question)
            ]
            resp = agent.invoke({"messages": message})
            msg = resp["messages"]
            resp1 = msg[-1]
            self._lastResponse += msg
            ret = resp1.content
        except Exception as e:
            ret = '输出错误: ' + str(e)
        return ret

    def outputResponse(self, resp: Any)->bool:
        if str == type(resp):
            colorPrint.green(resp)
            return True
        else:
            colorPrint.red(resp)
            return False