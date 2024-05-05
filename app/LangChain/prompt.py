#!/bin/env python
# -*- coding: utf-8
import re
from typing import List, Any
from langchain import hub
from langchain_core.messages import BaseMessage
from langchain.output_parsers import ResponseSchema
from langchain_core.prompt_values import PromptValue
from langchain.prompts import HumanMessagePromptTemplate
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import ChatPromptTemplate, PromptTemplate


class Prompt(object):
    """
    输出定制
    1. 输出JSON格式：
        从下列文本中提取如下信息：
        key1: 说明key1代表什么
        key2: 说明key2代表什么

        把提取到的信息格式化为 JSON 输出，必须包含以下键
        key1
        key2

        text: {text}

    2. 输出结构化格式：
        from langchain.output_parsers import ResponseSchema
        from langchain.output_parsers import StructuredOutputParser

        key1Schema = ResponseSchema(name='key1', description='说明key1代表什么')
        key2Schema = ResponseSchema(name='key2', description='说明key2代表什么')
        respSchemas = [key1Schema, key2Schema]
        formatInstructions = outputParser.get_format_instructions()

        提示语2：
            从下列文本中提取如下信息：
            key1: 说明key1代表什么
            key2: 说明key2代表什么

            text: {text}
            {formatInstructions}
        prompt = ChatPromptTemplate.from_template(template=提示语2)
        msg = prompt.format_messages(text=输入, format_instructions=formatInstructions)
        resp = chat(msg)

        resp 得到字典类型的数据格式，而不是字符串类型的数据格式
    """

    def __init__(self):
        # 正常聊天的提示模板
        self._defaultPromptStr = '''
        As a Chinese speaking AI, you should only use Chinese to answer my questions at any time:
        
        question: ```{text}```
        '''
        # 正常聊天使用了Agent的提示模板
        self._defaultAgentPromptStr = """
        As a powerful and Chinese-speaking AI, you should answer my questions only in Chinese at all times. \
        You can answer simple questions or provide in-depth explanations and discussions on complex, broad topics. \
        For example: when I type text, allow you to have a natural conversation about my input, extract the intent of my question, and complete the answer you think is best. \
        In this process, you should continue to learn and improve, and use the knowledge and tools you have to provide me with accurate information.

        TOOLS:
        ------
        Assistant has access to the following tools:
        {tools}
        
        To use a tool, please use the following format:
        ```
        Thought: Do I need to use a tool? Yes
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ```
        
        When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:
        ```
        Thought: Do I need to use a tool? No
        Final Answer: [your response here]
        ```
        
        Begin!

        New input: {input}
        {agent_scratchpad}
        """

    def getDefaultPrompt(self, question: str) -> PromptValue:
        prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template(self._defaultPromptStr)
            ],
            input_variables=[question])
        return prompt.format_prompt(text=question)

    def getDefaultPromptTemplate(self) -> PromptTemplate:
        return PromptTemplate.from_template(re.sub(r" +", ' ', self._defaultAgentPromptStr))

    """
    输入数据的格式：
    @param question: string 要处理的提问
    @return: PromptValue
    """
    def getOutputDictPrompt(self, question: str, args: list[tuple]) -> PromptValue | list[BaseMessage]:
        if len(args) <= 0:
            return self.getDefaultPrompt(question)
        schemaList = []
        promptStrT = ''
        for tp in args:
            if len(tp) == 3:
                ks = ResponseSchema(name=str(tp[0]), description=str(tp[1]), type=str(tp[2]))
                schemaList.append(ks)
                promptStrT += tp[0] + ": " + tp[1] + "\n"
            elif len(tp) == 2:
                ks = ResponseSchema(name=tp[0], description=tp[1], type='string')
                schemaList.append(ks)
                promptStrT += tp[0] + ": " + tp[1] + "\n"
            else:
                continue
        promptStr = ("""从下面的文本中提取如下信息:\n""" + promptStrT + """\n文本: {text}\n\n{formatInstructions}\n""")

        outputParser = StructuredOutputParser.from_response_schemas(schemaList)
        formatInstructions = outputParser.get_format_instructions()
        prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template(promptStr)
            ],
            input_variables=[question],
            partial_variables={'formatInstructions': formatInstructions})
        return prompt.format_prompt(text=question).to_messages()

    @staticmethod
    def formatOutputDictResult(resp: Any, args: list[tuple]) -> Any:
        if len(args) <= 0:
            return resp
        schemaList = []
        for tp in args:
            if len(tp) == 3:
                ks = ResponseSchema(name=tp[0], description=tp[1], type=tp[2])
                schemaList.append(ks)
            elif len(tp) == 2:
                ks = ResponseSchema(name=tp[0], description=tp[1], type='string')
                schemaList.append(ks)
            else:
                continue
        outputParser = StructuredOutputParser.from_response_schemas(schemaList)
        return outputParser.parse(resp)
