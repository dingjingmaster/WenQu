import sys
import ollama
from ollama import Client


class LLMOllama(object):
    def __init__(self):
        self.client = ollama.Client(host="http://127.0.0.1:11434")
        self.modelName = ""

    def setModel(self, modelName: str):
        self.modelName = modelName

    def getLocalModelList(self):
        return self.client.list()

    def chat(self, question: str):
        self.check()
        contentStr = f'''
        请使用中文回答此问题
        问题: {question}
        '''
        return self.client.chat(model=self.modelName, messages=[
            {
                'role': 'user',
                'content': contentStr
            }
        ])

    def check(self):
        if None is self.client or '' == self.modelName or None is self.modelName:
            print("请先调用 setModel() 方法设置要使用的LLM")
            sys.exit(1)


