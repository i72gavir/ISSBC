#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:03:34 2026

@author: rgalan
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QLineEdit, QComboBox,
    QHBoxLayout, QRadioButton, QMessageBox
)

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Sistema de Diagnóstico - Medicina Deportiva")

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()

        # Síntomas
        layout.addWidget(QLabel("Selecciona los síntomas:"))
        self.symptom_list = QListWidget()
        self.symptom_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

        # Ejemplo
        sintomas = [
           "Dolor muscular",
           "Fatiga excesiva",
           "Falta de rendimiento",
           "Lesiones recurrentes",
           "Calambres",
           "Falta de movilidad",
           "Dolor articular"
       ]

        for s in sintomas:
            self.symptom_list.addItem(QListWidgetItem(s))

        layout.addWidget(self.symptom_list)

        # Observables
        layout.addWidget(QLabel("Frecuencia cardíaca (bpm):"))
        self.hr_input = QLineEdit()
        layout.addWidget(self.hr_input)


        # Niveles
        layout.addWidget(QLabel("Nivel de fatiga:"))
        self.fatigue_combo = QComboBox()
        self.fatigue_combo.addItems(["Bajo", "Medio", "Alto"])
        layout.addWidget(self.fatigue_combo)

        layout.addWidget(QLabel("Nivel de hidratación:"))
        self.hydration_combo = QComboBox()
        self.hydration_combo.addItems(["Bajo", "Medio", "Alto"])
        layout.addWidget(self.hydration_combo)

        # Modo
        self.local_mode = QRadioButton("Local")
        self.web_mode = QRadioButton("Web")
        self.local_mode.setChecked(True)

        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.local_mode)
        mode_layout.addWidget(self.web_mode)
        layout.addLayout(mode_layout)

        # Botones
        button_layout = QHBoxLayout()
        self.btn_hypothesis = QPushButton("Evaluar hipótesis")
        self.btn_diagnose = QPushButton("Diagnosticar")
        self.btn_justify = QPushButton("Ver justificación")
        self.btn_pdfs = QPushButton("Gestión PDFs")
        self.btn_web = QPushButton("Fuentes web")

        button_layout.addWidget(self.btn_hypothesis)
        button_layout.addWidget(self.btn_diagnose)
        button_layout.addWidget(self.btn_justify)
        button_layout.addWidget(self.btn_pdfs)
        button_layout.addWidget(self.btn_web)

        layout.addLayout(button_layout)
        central.setLayout(layout)

        # Eventos
        self.btn_hypothesis.clicked.connect(self.evaluate)
        self.btn_diagnose.clicked.connect(self.diagnose)

    def get_inputs(self):
        symptoms = [item.text() for item in self.symptom_list.selectedItems()]
        observables = {
            "hr": self.hr_input.text(),
            "fatigue": self.fatigue_combo.currentText(),
            "hydration": self.hydration_combo.currentText()
        }
        mode = "WEB" if self.web_mode.isChecked() else "LOCAL"
        return symptoms, observables, mode

    def evaluate(self):
        symptoms, obs, mode = self.get_inputs()

        if not symptoms:
            QMessageBox.warning(self, "Error", "Selecciona al menos un síntoma")
            return

        self.controller.set_symptoms(symptoms, obs)
        self.controller.model.mode = mode
        self.controller.evaluate_hypotheses()
        self.controller.show_hypotheses()

    def diagnose(self):
        symptoms, obs, mode = self.get_inputs()

        if not symptoms:
            QMessageBox.warning(self, "Error", "Selecciona síntomas")
            return

        self.controller.set_symptoms(symptoms, obs)
        self.controller.model.mode = mode
        self.controller.diagnose()
        self.controller.show_diagnosis()