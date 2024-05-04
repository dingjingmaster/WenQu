import sys
import ollama
from ollama import Client
from app.Utils.print import Print
from app.LangChain.prompt import Prompt


class LLMOllama(object):
    def __init__(self):
        self.prompt = Prompt()
        self.client = ollama.Client(host="http://127.0.0.1:11434")
        self.modelName = ""

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

    def validate(self) -> bool:
        res = self.getLocalModelList()
        return len(res['models']) > 0

    def check(self):
        if None is self.client or '' == self.modelName or None is self.modelName or not self.validate():
            Print().red("请先 拉取模型 并 调用 setModel() 方法设置要使用的LLM")
            sys.exit(1)


