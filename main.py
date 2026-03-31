#!/bin/env python
# -*-coding:utf-8-*-
import sys
import time
import signal
import _thread
import readline
import markdown

from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QApplication

from app.Utils.print import colorPrint
from app.LLMManager.llama import LLMOpenAI
from PyQt6.QtCore import QThread, pyqtSignal

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton

from app.LLMManager.common import gIsDebug

gIsDebug = False



class LLMThread(QThread):
    sendToken = pyqtSignal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        llm = LLMOpenAI()
        # 暂不支持流式输出
        '''
        import asyncio
        async def runLLM():
            async for resp in llm.agentAsync(self.prompt):
                self.sendToken.emit(str(resp))
        asyncio.run(runLLM())
        '''
        res = llm.agent(self.prompt)
        self.sendToken.emit(res)


class LangChainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WenQu")
        self.resize(600, 400)

        self.layout = QVBoxLayout()
        self.textArea = QTextEdit()
        self.textArea.setReadOnly(True)

        self.inputLine = QLineEdit()
        self.inputLine.setPlaceholderText("输入问题…")
        self.sendButton = QPushButton("提交")

        self.layout.addWidget(self.textArea)
        self.layout.addWidget(self.inputLine)
        self.layout.addWidget(self.sendButton)
        self.setLayout(self.layout)

        self.sendButton.clicked.connect(self.startLLM)
        self.inputLine.returnPressed.connect(self.startLLM)

    def startLLM(self):
        prompt = self.inputLine.text().strip()
        if not prompt:
            return

        self.textArea.append(f"你: {prompt}\n")
        self.inputLine.clear()

        self.thread = LLMThread(prompt)
        self.thread.sendToken.connect(self.updateText)
        self.thread.start()

    def updateText(self, token):
        cursor = self.textArea.textCursor()
        # cursor.movePosition(QTextCursor.End)
        self.textArea.insertPlainText("\n")
        html = markdown.markdown(token, extensions=["extra", "codehilite", "nl2br", "sane_lists", "def_list", "attr_list"])
        self.textArea.insertHtml(html)


def signal_exit(sig, frame):
    sys.exit(0)

def signal_handler(sig, frame):
    if sig == signal.SIGINT \
            or sig == signal.SIGTERM:
        print("", end='\r\033[K')
        colorPrint.red("如果您想退出，请输入 '/bye' 结束进程!")
    elif sig == signal.SIGQUIT \
            or sig == signal.SIGHUP \
            or sig == signal.SIGTSTP \
            or sig == signal.SIGKILL \
            or sig == signal.SIGSTOP:
        colorPrint.green("\nbye!", end="\n\n")
        sys.exit(0)


def loading(lock):
    status = ['⢹', '⣸', '⣴', '⣦', '⣇', '⡏', '⠟', '⠻']
    i = 0
    print('\r\033[1K', end='', flush=True)
    while lock[0]:
        i = (i + 1) % len(status)
        print('\r\033[1;32m %s %s\033[0m' % (status[i], lock[1] or '' if len(lock) >= 2 else ''), end='', flush=True)
        time.sleep(0.1)
    print("", end='', flush=True)


def startWait(lock):
    lock[0] = True
    try:
        _thread.start_new_thread(loading, (lock,))
    except Exception as e:
        pass


def stopWait(lock):
    lock[0] = False
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()


if __name__ == "__main__":
    gsLock = [True, '正在请求...']
    signal.signal(signal.SIGTERM, signal_exit)
    signal.signal(signal.SIGQUIT, signal_exit)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGTSTP, signal_handler)
    signal.signal(signal.SIGABRT, signal_handler)

    app = QApplication(sys.argv)
    gui = LangChainGUI()

    gui.show()
    '''
    print("欢迎使用WenQu!")
    llm = LLMOpenAI()
    while True:
        line = input("> ")
        if "/bye" == line:
            break
        elif "" == line:
            continue
        # request
        startWait(gsLock)
        # resp = llm.chat(line)
        resp = llm.agent(line)
        stopWait(gsLock)
        llm.outputResponse(resp)
        print('', flush=True)
    '''
    exit(app.exec())
