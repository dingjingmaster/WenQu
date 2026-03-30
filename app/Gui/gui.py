#!/usr/bin/env python
# -*- coding=utf-8 -*-

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton


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

        # self.thread = LLMThread(prompt)
        # self.thread.sendOutput.connect(self.updateText)
        # self.thread.start()

    def update_text(self, token):
        self.textArea.moveCursor(self.textArea.textCursor().End)
        self.textArea.insertPlainText(token)