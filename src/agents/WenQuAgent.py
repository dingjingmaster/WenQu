import os

import langchain_core
import psycopg2
import chainlit as cl
from urllib.parse import urlparse

from langchain_core.messages import HumanMessage
from langchain_core.tracers import langchain
from langchain_openai import ChatOpenAI
from deepagents import create_deep_agent
from src.config.WenQuConfig import getGlobalConfig
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.postgres import PostgresSaver
from langchain.agents.middleware import SummarizationMiddleware

dbName = "WenQu"
sessionDBUrl = "postgresql://postgres@127.0.0.1:5432/WenQu?sslmode=disable"
systemPrompt ='''
你是一位乐于助人、准确无误且值得信赖的智能助手。

# 🈯 语言要求（强制）
- 你必须始终使用【中文】回复用户(包括你的思考过程)。
- 不允许使用英文回答正文内容。
- 专有名词可以保留英文（如 API 名称、代码、函数名），但解释必须是中文。
- 如果用户使用其他语言提问，也必须用中文回答。

# 🎯 核心行为原则
- 优先保证答案的准确性，而不是长度或表达优美。
- 不确定的信息必须明确说明“不确定”，禁止编造。
- 不允许捏造工具结果、数据或事实。

# 🧠 思考方式
- 对复杂问题必须分步骤思考并组织答案。
- 优先使用简单、清晰、可执行的方案。
- 避免无意义扩展内容。

# 🧰 工具使用规则（如存在工具）
- 只有在确实需要时才调用工具。
- 不允许假设工具返回结果。
- 工具失败必须明确说明，并尝试替代方案。

# 📚 上下文规则
- 只基于当前对话上下文回答问题。
- 不允许编造上下文中不存在的信息。
- 信息不足时必须主动询问用户。

# 💻 代码规则
- 需要代码时必须提供可运行的代码。
- 默认使用中文解释代码逻辑。
- 除非用户要求，否则不使用伪代码。

# 🧾 输出格式
- 回答必须结构清晰（可使用分点、步骤、代码块）。
- 避免重复内容。
- 避免无意义冗长解释。

# ⚠️ 安全规则
- 不提供违法、危险或不安全内容。
- 遇到违规请求时必须简短拒绝并说明原因。

# 🎯 风格要求
- 语气专业、清晰、直接。
- 不要啰嗦，不要重复强调同一信息。
- 不要使用英文作为默认回答语言。
                '''

def createDB():
    url = urlparse(sessionDBUrl)
    admin_db = "postgres"
    conn = psycopg2.connect(
        dbname=admin_db,
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbName,))
    exists = cur.fetchone()
    if not exists:
        cur.execute(f'CREATE DATABASE "{dbName}"')
    cur.close()
    conn.close()


class WenQuAgent(object):
    def __init__(self, sessionId: str):
        createDB()
        os.environ["OPENAI_API_KEY"] = "sk-local"
        self._cmdStep = cl.Step(name="工具📌")
        self._outBuffer = cl.Message(content="")
        self._config = getGlobalConfig()
        self._sessionId = sessionId
        self._tools = []
        print("sessionId: " + sessionId)
        self._agentConfig : RunnableConfig = {"configurable" : {"thread_id" : sessionId}}
        self._masterAgent = ChatOpenAI(
            model='WenQuAgent',
            base_url=self._config.getMainLlmUrl(),
            max_retries=99,
            timeout=200,
            streaming=True,
        )
        self._middleware = [
            SummarizationMiddleware(model=self._masterAgent,
                                    max_summary_tokens=200,
                                    max_tokens_before_summary=409600)
        ]
        self._subagents = {
            "main": self._masterAgent,
        }
    async def _updateCmdStep(self, msg : str):
        self._cmdStep.output = msg
        await self._cmdStep.send()
        await self._cmdStep.update()

    async def _updateOutBuffer(self, chunk: str):
        await self._outBuffer.stream_token(str(chunk))

    def chatAsync(self, question: str):
        with PostgresSaver.from_conn_string(sessionDBUrl) as conn:
            conn.setup()
            agent = create_deep_agent(
                model=self._masterAgent,
                tools=self._tools,
                middleware=self._middleware,
                checkpointer=conn,
                system_prompt=systemPrompt
            )
            try:
                res = agent.invoke(
                    {
                        "messages": [
                            HumanMessage(
                                content=question,
                            )
                        ]
                    },
                    config=self._agentConfig
                )
                resMsg = res["messages"]
                respMsg = resMsg[-1]
                return str(respMsg.content)
            except Exception as e:
                return "Error: " + str(e)

    async def waitFinished(self):
        await self._outBuffer.send()

    async def _messageAsync(self, msg : langchain_core.messages.ai.AIMessage):
        if not isinstance(msg, langchain_core.messages.ai.AIMessage):
            return
        if hasattr(msg, "content"):
            if 'tool_calls' in msg:
                cmdCalls = msg.tool_calls
                cmd = ''
                for c in cmdCalls:
                    print("==>" + str(c))
                    if 'name' in c:
                        cmd += '命令：' + str(c['name'])
                        continue
                    elif 'args' in c:
                        cmd += '参数： ' + str(' '.join(c['args']))
                        continue
                    cmd += '\n'
                if '' != cmd:
                    await self._updateCmdStep(cmd)
            await self._updateOutBuffer(str(msg.content))
    async def _messageCommand(self, msgs : list):
        toolsNames = []
        if isinstance(msgs, list):
            for t in msgs:
                if hasattr(t, "name") and hasattr(t, "content") and len(t.content) > 0:
                    msg = "%s %s\n" % (t.name, ' '.join(t.content))
                    toolsNames.append(msg)
        if len(toolsNames) > 0:
            await self._updateCmdStep('命令: %s' % (', '.join(toolsNames)))

    async def chatSync(self, question:str):
        with PostgresSaver.from_conn_string(sessionDBUrl) as conn:
            conn.setup()
            agent = create_deep_agent(
                    model=self._masterAgent,
                    tools=self._tools,
                    middleware=self._middleware,
                    checkpointer=conn,
                    system_prompt=systemPrompt
            )
            for chunk in agent.stream(
                    {
                            "messages": [
                                HumanMessage(
                                    content=question,
                                )
                            ]
                        },
                        stream_mode="updates",
                        subgraphs=True,
                        version="v2",
                        config=self._agentConfig,

                    ):
                if not chunk:
                    continue
                '''
                nodeName:
                    - type: 事件类型(这次流的是什么)
                    - ns: namespace(事件来自哪个节点/步骤/子图)
                    - data: 实际内容(token/message/state更新)
                nodeData:
                    - type: --> updates
                    - ns: --> ()
                    - data: --> dict{}
                '''
                for nodeName, nodeData in chunk.items():
                    if nodeName == 'data':
                        if 'model' in nodeData:
                            modelData = nodeData['model']
                            if 'messages' in modelData:
                                for msg in modelData['messages']:
                                    print(type(msg))
                                    await self._messageAsync(msg)
                            else:
                                # print(nodeData)
                                # print("\n")
                                pass
                        elif 'tools' in nodeData:
                            tools = nodeData['tools']
                            if 'messages' in tools:
                                await self._messageCommand(tools['messages'])
                        else:
                            # print(nodeData)
                            # print("\n")
                            pass
                    else:
                        # print(nodeData)
                        # print("\n")
                        pass
        pass