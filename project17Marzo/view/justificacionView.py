# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 17:47:34 2026

@author: Rafa
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit

class JustificationWindow(QDialog):
    def __init__(self, justification):
        super().__init__()
        self.setWindowTitle("Justificación")

        layout = QVBoxLayout()

        text = QTextEdit()
        text.setReadOnly(True)
        text.setText(justification)

        layout.addWidget(text)
        self.setLayout(layout)