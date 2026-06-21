# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTextEdit,
    QLineEdit, QPushButton, QHBoxLayout
)

class ChatWindow(QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Asistente Inteligente")
        self.resize(500, 600)

        layout = QVBoxLayout()

        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Escribe tu mensaje...")

        self.btn_send = QPushButton("Enviar")

        bottom = QHBoxLayout()
        bottom.addWidget(self.input)
        bottom.addWidget(self.btn_send)

        layout.addWidget(self.chat_box)
        layout.addLayout(bottom)

        self.setLayout(layout)

        self.btn_send.clicked.connect(self.send_message)

    def send_message(self):
        msg = self.input.text().strip()
        if not msg:
            return

        self.chat_box.append(f"Tú: {msg}")

        response = self.controller.send_chat_message(msg)

        self.chat_box.append(f"IA: {response}\n")

        self.input.clear()