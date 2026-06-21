#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 17:46:57 2026

@author: rgalan
"""

from PyQt5.QtWidgets import ( 
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt

class HypothesisWindow(QDialog):
    def __init__(self, hypotheses, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Hipótesis")
        
        # Agrandar tamaño ventana
        self.resize(800,500)

        layout = QVBoxLayout()

       # Tabla de hipótesis
        self.table = QTableWidget()
        self.table.setRowCount(len(hypotheses))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Hipótesis", "Score"])
        self.table.horizontalHeader().setStretchLastSection(True)  # última columna se expande
        self.table.setWordWrap(True)  # habilita salto de línea

        for i, h in enumerate(hypotheses):
            item_name = QTableWidgetItem(h["name"])
            item_name.setFlags(item_name.flags() ^ Qt.ItemFlag.ItemIsEditable)
            item_name.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            item_name.setToolTip(h["name"])  # Muestra todo el texto al pasar el mouse

            item_score = QTableWidgetItem(str(h["score"]))
            item_score.setFlags(item_score.flags() ^ Qt.ItemFlag.ItemIsEditable)
            item_score.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(i, 0, item_name)
            self.table.setItem(i, 1, item_score)

        # Ajustar tamaño de columnas y filas de manera auto
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        layout.addWidget(self.table)

        # Botones horizontal: Diagnosticar / Volver
        button_layout = QHBoxLayout()
        self.btn_diagnose = QPushButton("Diagnosticar")
        self.btn_back = QPushButton("Volver")
        button_layout.addWidget(self.btn_diagnose)
        button_layout.addWidget(self.btn_back)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Eventos
        self.btn_diagnose.clicked.connect(self.on_diagnose)
        self.btn_back.clicked.connect(self.close)

    def on_diagnose(self):
        # Llama al controlador para generar diagnóstico
        self.controller.diagnose()
        # Cierra ventana de hipótesis y abre ventana de diagnóstico
        self.close()
        self.controller.show_diagnosis()