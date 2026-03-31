from typing import Any


import os
import datetime
import langchain

from langchain.agents.middleware import SummarizationMiddleware
from langchain_classic.agents import AgentExecutor

from langchain_core.runnables import RunnableConfig

from app.LangChain.agent import LlamaDeepAgent
from app.Utils.print import colorPrint
from langchain_openai import ChatOpenAI
from deepagents import create_deep_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.postgres import PostgresSaver

from app.LLMManager.common import gIsDebug

from app.LangChain.tools import gFs, read_file, delete_file, current_date, current_date_time

from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import BaseCallbackHandler


DB_URI = "postgresql://postgres@127.0.0.1:5432/wenqu?sslmode=disable"


class StreamHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token, **kwargs):
        print(token, end="", flush=True)


class LLMOpenAI(object):
    def __init__(self):
        langchain.debug = gIsDebug
        os.environ["OPENAI_API_KEY"] = "sk-local"
        agentTools = [
            read_file,
            delete_file,
            current_date,
            current_date_time,
        ]
        tools = []
        self.__agentTools = tools + agentTools
        self.__interruptTool = {
            "delete_file": True,
            "read_file": False,
        }
        _key = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        self._config: RunnableConfig = {"configurable": {"thread_id": _key}}

        prompt = """你必须严格按照以下格式回答：

        Question: {input}
        Thought: 思考
        Action: 工具名
        Action Input: 输入
        Observation: 结果
        ...
        Final Answer: 最终答案
        """

        self._client = LlamaCpp(model_path="./models/Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf",
                                temperature=0.6,
                                max_tokens=64000,
                                n_ctx=4096,
                                prompt=prompt,
                                n_gpu_layers=64,
                                n_threads=16,
                                use_mlock=True,
                                tensor_split=None,
                                low_vram=False,
                                use_gpu=True,
                                callbacks=[StreamHandler()])
        #ChatOpenAI(model="localLLM", base_url="http://127.0.0.1:9999/v1", max_retries=99, timeout=200, streaming=True)
        self._middleware = [
            SummarizationMiddleware(model=self._client, trigger=("tokens", 40960), keep=("messages", 60)),
        ]

    def chat(self, question: str):
        resp = self._client.invoke(input=question)
        return resp.content

    def agent(self, question:str) -> str:
        ret = "数据库连接失败."
        try:
            message = []
            message += [
                HumanMessage(question)
            ]
            with PostgresSaver.from_conn_string(DB_URI) as conn:
                conn.setup()
                agent = LlamaDeepAgent(llm=self._client, tools=self.__agentTools)
                # agent = create_deep_agent(model=self._client,
                #                           backend=gFs,
                #                           tools=self.__agentTools,
                #                           interrupt_on=self.__interruptTool,
                #                           middleware=self._middleware, checkpointer=conn, )
                # resp = agent.invoke({"messages": message}, config=self._config, timeout=-1)
                resp = agent.invoke(question)
                print("-----------------------------------------\n")
                print(resp, flush=True)

                # msg = resp["messages"]
                # resp1 = msg[-1]
                # ret = resp1.content
        except Exception as e:
            ret = '输出错误: ' + str(e)
        return ret

    # 目前不支持流式输出
    # async def agentAsync(self, question:str):
    #     try:
    #         message = []
    #         message += [
    #             HumanMessage(question)
    #         ]
    #         with PostgresSaver.from_conn_string(DB_URI) as conn:
    #             conn.setup()
    #             agent = create_deep_agent(model=self._client,
    #                                       backend=gFs,
    #                                       tools=self.__agentTools,
    #                                       interrupt_on=self.__interruptTool,
    #                                       middleware=self._middleware, checkpointer=conn, )
    #             print(question)
    #             async for chunk in agent.astream(question, config=self._config, stream_mode="values"):
    #                 print("-->" + chunk.content, flush=True)
    #                 yield str(chunk)
    #     except Exception as e:
    #         yield str(e)

    def outputResponse(self, resp: Any)->bool:
        if str == type(resp):
            colorPrint.green(resp)
            return True
        else:
            colorPrint.red(resp)
            return False