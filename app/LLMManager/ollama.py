import sys
from typing import Any

import ollama
import langchain
from ollama import Client
from app.Utils.print import Print
from app.LangChain.tools import *
from langchain.agents import AgentType
from app.Utils.print import colorPrint
from app.LangChain.prompt import Prompt
from langchain_core.messages import HumanMessage
from langchain_community.chat_models import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, load_tools, create_react_agent


class LLMOllama(object):
    def __init__(self):
        langchain.debug = False
        agentTools = [
            tool_current_date,
            tool_current_date_time,
        ]
        self.modelName = ""
        self.prompt = Prompt()
        self.client = ollama.Client(host="http://127.0.0.1:11434")
        self.setDefaultModel()
        if "" == self.modelName:
            colorPrint.red("请先执行 ollama pull <模型名> 拉取模型")
            sys.exit(1)
        llm = ChatOllama(model=self.modelName, temperature=0)
        tools = [] #load_tools(['llm-math', 'wikipedia'], llm=llm)
        self.__agentTools = tools + agentTools
        self.__llmAgent = create_react_agent(llm=llm, tools=self.__agentTools, prompt=self.prompt.getDefaultPromptTemplate())

    def setModel(self, modelName: str):
        self.modelName = modelName

    def setDefaultModel(self) -> str:
        res = self.getLocalModelList()
        models = res['models']
        if len(models) > 0:
            self.setModel(models[0]['name'])
        return self.modelName

    def getLocalModelList(self):
        return self.client.list()

    def chat(self, question: str):
        self.check()
        questionStr = self.prompt.getDefaultPrompt(question).to_string()
        return self.client.chat(model=self.modelName, messages=[
            {
                'role': 'user',
                'content': questionStr
            }
        ])

    def agent(self, question: str):
        self.check()
        agentExecutor = AgentExecutor(agent=self.__llmAgent, tools=self.__agentTools, handle_parsing_errors=True if langchain.debug else False)
        return agentExecutor.invoke(
            {
                'input': question,
            }
        )

    def validate(self) -> bool:
        res = self.getLocalModelList()
        return len(res['models']) > 0

    def check(self):
        if None is self.client or '' == self.modelName or None is self.modelName or not self.validate():
            Print().red("请先 拉取模型 并 调用 setModel() 方法设置要使用的LLM")
            sys.exit(1)
        pass

    def outputResponse(self, resp: Any) -> bool:
        if str == type(resp):
            colorPrint.green(resp)
            return True
        elif dict == type(resp):
            if 'message' in resp and 'content' in resp['message']:
                colorPrint.green(resp['message']['content'])
                return True
            elif 'output' in resp:
                colorPrint.green(resp['output'])
                return True

        colorPrint.yellow(type(resp))
        colorPrint.yellow(str(resp))
        return False



