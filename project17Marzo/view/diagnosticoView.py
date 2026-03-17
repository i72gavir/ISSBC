# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 17:47:15 2026

@author: Rafa
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit

class DiagnosisWindow(QDialog):
    def __init__(self, diagnosis, confidence):
        super().__init__()
        self.setWindowTitle("Diagnóstico")

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Diagnóstico: {diagnosis}"))
        layout.addWidget(QLabel(f"Confianza: {confidence}"))

        self.recommendation = QTextEdit()
        self.recommendation.setPlaceholderText("Recomendación...")
        layout.addWidget(self.recommendation)

        self.setLayout(layout)