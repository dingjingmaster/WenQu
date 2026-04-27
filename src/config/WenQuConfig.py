import os
import configparser

baseDir = os.path.dirname(os.path.abspath(__file__))
configPath = os.path.abspath(os.path.join(baseDir, "../../config/config.ini"))

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class WenQuConfig(metaclass=SingletonMeta):
    def __init__(self, config: str):
        self._configPath = config
        print("path: " + self._configPath)
        self._configObj = configparser.ConfigParser()

        # 主模型链接
        self._mainLlmUrl = ''

    def loadConfig(self) -> bool:
        self._configObj.read(self._configPath, encoding="utf-8")
        self._mainLlmUrl = self._configObj.get('llm', "baseUrl")
        return True

    def getMainLlmUrl(self) -> str:
        return self._mainLlmUrl

def getGlobalConfig() -> WenQuConfig:
    return WenQuConfig(configPath)
