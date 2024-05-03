#!/bin/env python
# -*-coding:utf-8-*-
import sys
import signal
import readline


def signal_handler(sig, frame):
    if sig == signal.SIGINT \
            or sig == signal.SIGTSTP \
            or sig == signal.SIGTERM:
        print("", end='\r\033[K')
        print("如果您想退出，请输入 '/bye' 结束进程!")
    elif sig == signal.SIGQUIT \
            or sig == signal.SIGHUP \
            or sig == signal.SIGKILL \
            or sig == signal.SIGSTOP:
        print("\nbye!", end="\n\n")
        sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGTSTP, signal_handler)
    signal.signal(signal.SIGABRT, signal_handler)
    print("欢迎使用WenQu!")
    while True:
        line = input("> ")
        if "/bye" == line:
            break
        elif "" == line:
            continue
        print(line, end="\n\n")
    exit(0)
