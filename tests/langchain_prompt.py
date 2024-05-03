from app.LangChain.prompt import Prompt
from app.LLMManager.ollama import LLMOllama

if __name__ == '__main__':
    prompt = Prompt()

    print(prompt.getDefaultPrompt("你好！"))

    strs = "你好！, k=1231231; k2=english; k3=math"
    dictFormat = [("k1", "k1的值"), ("k2", "k2的值"), ("k3", "k3的值", "string")]
    p = prompt.getOutputDictPrompt(strs, dictFormat)

    print(type(p))
    print(p)

    llm = LLMOllama()
    llm.setModel("llama3:instruct")
    resp = llm.chat(p)

    print(resp)
    respT = resp['message']['content']
    print(type(respT))
    print(respT)

    respFormat = prompt.formatOutputDictResult(respT, dictFormat)
    print(type(respFormat))
    print(respFormat)
