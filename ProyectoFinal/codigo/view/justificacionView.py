# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 17:47:34 2026

@author: Rafa
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QLabel


class JustificationWindow(QDialog):
    def __init__(self, justification, diagnosis, confidence, url):
        super().__init__()

        self.setWindowTitle("Justificación del Diagnóstico")
        self.resize(600, 500)

        layout = QVBoxLayout()

        # ---------------- DIAGNÓSTICO ----------------
        layout.addWidget(QLabel(f"<h2>Diagnóstico: {diagnosis}</h2>"))
        layout.addWidget(QLabel(f"Confianza: {(confidence or 0.0):.2f}"))

        # ---------------- PDF ORIGEN ----------------
        layout.addWidget(QLabel(f" Fuente (PDF): {url}"))

        # ---------------- JUSTIFICACIÓN ----------------
        layout.addWidget(QLabel("<b>Explicación clínica:</b>"))
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setText(justification)

        layout.addWidget(self.text)

        self.setLayout(layout)