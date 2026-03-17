#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:03:24 2026

@author: rgalan
"""


from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QListWidget, QListWidgetItem, QDoubleSpinBox
)
from PyQt5.QtCore import Qt

class VistaPrincipal(QWidget):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador

        self.setWindowTitle("Diagnóstico Deportivo")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Selecciona síntomas:"))

        self.lista_sintomas = QListWidget()
        self.lista_sintomas.setSelectionMode(QListWidget.MultiSelection)

        sintomas = [
            "dolor", "inflamacion", "rigidez",
            "limitacion_movimiento", "dolor_movimiento"
        ]

        for s in sintomas:
            item = QListWidgetItem(s)
            self.lista_sintomas.addItem(item)

        layout.addWidget(self.lista_sintomas)

        layout.addWidget(QLabel("Temperatura corporal (°C):"))
        self.temperatura = QDoubleSpinBox()
        self.temperatura.setRange(35.0, 42.0)
        self.temperatura.setValue(36.5)
        layout.addWidget(self.temperatura)

        self.boton = QPushButton("Evaluar hipótesis")
        self.boton.clicked.connect(self.evaluar)
        layout.addWidget(self.boton)

        self.setLayout(layout)

    def evaluar(self):
        sintomas = [
            item.text()
            for item in self.lista_sintomas.selectedItems()
        ]

        temperatura = self.temperatura.value()

        self.controlador.evaluar(sintomas, temperatura)
        
        
        
        
class VistaResultados(QWidget):
    def __init__(self, resultados):
        super().__init__()

        self.setWindowTitle("Resultados del diagnóstico")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Hipótesis ordenadas:"))

        for nombre, score in resultados:
            texto = f"{nombre} → Probabilidad: {score}"
            layout.addWidget(QLabel(texto))

        self.setLayout(layout)
