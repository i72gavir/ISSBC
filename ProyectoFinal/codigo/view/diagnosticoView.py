# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 17:47:15 2026

@author: Rafa
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit


class DiagnosisWindow(QDialog):
    def __init__(self, diagnosis, confidence, justification, url):
        super().__init__()

        self.setWindowTitle("Diagnóstico")

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Diagnóstico: {diagnosis}"))
        layout.addWidget(QLabel(f"Confianza: {confidence}"))

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setText(justification)
        

        layout.addWidget(self.text)

        if url:
            layout.addWidget(QLabel("<b>Fuente:</b>"))
            layout.addWidget(QLabel(url))
        else:
            layout.addWidget(QLabel("<b>Fuente:</b> No disponible"))

        self.setLayout(layout)