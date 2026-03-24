#!/bin/env python
# -*-coding:utf-8-*-
import re
import sys
import time
import signal
import _thread
import readline

from app.Utils.print import colorPrint
from app.LLMManager.llama import LLMOpenAI

from app.LLMManager.common import gIsDebug

gIsDebug = False


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
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    #:]\signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGTSTP, signal_handler)
    signal.signal(signal.SIGABRT, signal_handler)
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
    exit(0)
