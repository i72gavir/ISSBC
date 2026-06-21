# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:03:34 2026

@author: rgalan
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QFileDialog, QMessageBox, QGroupBox, QHBoxLayout, QTextEdit
)
from datetime import datetime
import json


class MedicoView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Panel Médico")
        self.resize(700, 500)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        # ---------------- PACIENTE ----------------
        patient_group = QGroupBox("Paciente")
        patient_layout = QHBoxLayout()

        self.patient_input = QLineEdit()
        self.patient_input.setPlaceholderText("Nombre del paciente")

        patient_layout.addWidget(QLabel("Nombre:"))
        patient_layout.addWidget(self.patient_input)

        patient_group.setLayout(patient_layout)

        # ---------------- BOTONES ----------------
        actions_group = QGroupBox("Acciones")
        actions_layout = QHBoxLayout()

        self.btn_save = QPushButton("Guardar")
        self.btn_load = QPushButton("Cargar")

        self.btn_save.clicked.connect(self.save_to_file)
        self.btn_load.clicked.connect(self.load_from_file)

        actions_layout.addWidget(self.btn_save)
        actions_layout.addWidget(self.btn_load)

        actions_group.setLayout(actions_layout)

        # ---------------- RESULTADO ----------------
        result_group = QGroupBox("Información del diagnóstico")
        result_layout = QVBoxLayout()

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        result_layout.addWidget(self.result_text)
        result_group.setLayout(result_layout)

        # ---------------- LAYOUT FINAL ----------------
        main_layout.addWidget(patient_group)
        main_layout.addWidget(actions_group)
        main_layout.addWidget(result_group)

        central.setLayout(main_layout)

        # Estilo
        self.apply_style()

    # ---------------- ESTILO ----------------
    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
                font-size: 14px;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ccc;
                border-radius: 8px;
                margin-top: 10px;
                padding: 10px;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
            QTextEdit {
                background-color: #f9f9f9;
                border-radius: 6px;
                padding: 8px;
            }
        """)

    # ---------------- DATOS ----------------
    def get_current_data(self):
        return self.controller.get_current_data()

    # ---------------- GUARDAR ----------------
    def save_to_file(self):
        name = self.patient_input.text()
        if not name:
            QMessageBox.warning(self, "Error", "Nombre requerido")
            return

        data = self.get_current_data()
        
        data["patient"] = name
        
        date = datetime.now().strftime("%Y-%m-%d")

        filename = f"{name}_{date}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        QMessageBox.information(self, "OK", f"Guardado en {filename}")

    # ---------------- CARGAR ----------------
    def load_from_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Abrir", "", "JSON (*.json)")
        if not file:
            return

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Rellenar nombre si viene en el archivo
        if "patient" in data:
            self.patient_input.setText(data["patient"])

        # Mostrar bonito
        self.display_data(data)

        # Pasar al controller (opcional)
        self.controller.load_data(data)

    # ---------------- MOSTRAR BONITO ----------------
    def display_data(self, data):
        symptoms = data.get("symptoms", [])
        obs = data.get("observables", {})
    
        lines = []
    
        lines.append("PACIENTE")
        lines.append("-------------------------")
        lines.append(f"Nombre: {self.patient_input.text()}")
        lines.append("")
    
        lines.append("CONTEXTO")
        lines.append("-------------------------")
        lines.append(f"Actividad: {obs.get('activity', '-')}")
        lines.append(f"Zona: {obs.get('body_part', '-')}")
        lines.append(f"Fatiga: {obs.get('fatigue', '-')}")
        lines.append(f"Hidratación: {obs.get('hydration', '-')}")
        lines.append("")
    
        lines.append("SÍNTOMAS")
        lines.append("-------------------------")
    
        for s in symptoms:
            lines.append(f"  • {s}")
    
        self.result_text.setText("\n".join(lines))