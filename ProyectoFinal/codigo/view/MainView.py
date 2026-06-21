#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:03:34 2026

@author: rgalan
"""


from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QComboBox,
    QHBoxLayout, QRadioButton, QMessageBox, QGroupBox, QCheckBox,
    QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Sistema de Diagnóstico - Medicina Deportiva")
        self.setMinimumSize(700, 800)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # ---------------- HEADER ----------------
        header_layout = QHBoxLayout()

        title = QLabel("Sistema de Diagnóstico Deportivo")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.dark_mode_toggle = QCheckBox("Modo oscuro")
        self.dark_mode_toggle.stateChanged.connect(self.toggle_dark_mode)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.dark_mode_toggle)

        layout.addLayout(header_layout)

        # ---------------- CONTEXTO ----------------
        context_group = QGroupBox("Contexto de la lesión")
        context_layout = QVBoxLayout()

        self.activity_combo = QComboBox()
        self.activity_combo.addItems([
            "Correr", "Sprint", "Fútbol", "Baloncesto", "Ciclismo",
            "Gimnasio - Pesas", "Estiramientos", "CrossFit",
            "Natación", "Deporte de contacto"
        ])

        self.body_part_combo = QComboBox()
        self.body_part_combo.addItems([
            "Rodilla", "Tobillo", "Pie", "Muslo (cuádriceps)",
            "Isquiotibiales", "Pantorrilla", "Cadera",
            "Zona lumbar", "Hombro", "Codo", "Muñeca"
        ])

        context_layout.addWidget(QLabel("Actividad:"))
        context_layout.addWidget(self.activity_combo)
        context_layout.addWidget(QLabel("Zona afectada:"))
        context_layout.addWidget(self.body_part_combo)

        context_group.setLayout(context_layout)
        layout.addWidget(context_group)

        # ---------------- SÍNTOMAS ----------------
        symptoms_group = QGroupBox("Síntomas")
        symptoms_layout = QVBoxLayout()

        self.symptom_list = QListWidget()
        self.symptom_list.setSelectionMode(QListWidget.MultiSelection)

        sintomas = [
            "Dolor agudo repentino", "Dolor progresivo", "Inflamación",
            "Hematoma", "Limitación del movimiento", "Inestabilidad articular",
            "Sensación de chasquido", "Rigidez muscular",
            "Debilidad muscular", "Dolor al apoyar peso", "Dolor al estirar"
        ]

        for s in sintomas:
            self.symptom_list.addItem(QListWidgetItem(s))

        symptoms_layout.addWidget(self.symptom_list)
        symptoms_group.setLayout(symptoms_layout)
        layout.addWidget(symptoms_group)

        # ---------------- NIVELES ----------------
        levels_group = QGroupBox("Estado físico")
        levels_layout = QVBoxLayout()

        self.fatigue_combo = QComboBox()
        self.fatigue_combo.addItems(["Bajo", "Medio", "Alto"])

        self.hydration_combo = QComboBox()
        self.hydration_combo.addItems(["Bajo", "Medio", "Alto"])

        levels_layout.addWidget(QLabel("Fatiga:"))
        levels_layout.addWidget(self.fatigue_combo)
        levels_layout.addWidget(QLabel("Hidratación:"))
        levels_layout.addWidget(self.hydration_combo)

        levels_group.setLayout(levels_layout)
        layout.addWidget(levels_group)

        # ---------------- MODO ----------------
        mode_login_layout = QHBoxLayout()

        mode_group = QGroupBox("Modo")
        mode_layout = QVBoxLayout()
        
        self.local_mode = QRadioButton("Local")
        self.web_mode = QRadioButton("Web")
        self.local_mode.setChecked(True)
        
        mode_layout.addWidget(self.local_mode)
        mode_layout.addWidget(self.web_mode)
        mode_group.setLayout(mode_layout)
        
        self.btn_login = QPushButton("Acceder")
        self.btn_chat = QPushButton("Chat IA")
        
        mode_login_layout.addWidget(mode_group)
        mode_login_layout.addWidget(self.btn_login)
        mode_login_layout.addWidget(self.btn_chat)
        
        self.btn_chat.clicked.connect(self.controller.open_chat)
        
        layout.addLayout(mode_login_layout)

        # ---------------- BOTONES ----------------
        main_buttons = QHBoxLayout()
        self.btn_hypothesis = QPushButton("Evaluar hipótesis")
        self.btn_diagnose = QPushButton("Diagnosticar")

        main_buttons.addWidget(self.btn_hypothesis)
        main_buttons.addWidget(self.btn_diagnose)

        secondary_buttons = QHBoxLayout()
        self.btn_justify = QPushButton("Ver justificación")
        self.btn_pdfs = QPushButton("Gestión PDFs")
        self.btn_web = QPushButton("Fuentes web")

        secondary_buttons.addWidget(self.btn_justify)
        secondary_buttons.addWidget(self.btn_pdfs)
        secondary_buttons.addWidget(self.btn_web)

        layout.addLayout(main_buttons)
        layout.addLayout(secondary_buttons)

        central.setLayout(layout)

        # Eventos
        self.btn_hypothesis.clicked.connect(self.evaluate)
        self.btn_diagnose.clicked.connect(self.diagnose)

        # Estilo inicial
        self.apply_light_theme()

    # ---------------- FUNCIONALIDAD ----------------
    def get_inputs(self):
        symptoms = [item.text() for item in self.symptom_list.selectedItems()]

        observables = {
            "fatigue": self.fatigue_combo.currentText(),
            "hydration": self.hydration_combo.currentText(),
            "activity": self.activity_combo.currentText(),
            "body_part": self.body_part_combo.currentText()
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

    def diagnose(self):
        symptoms, obs, mode = self.get_inputs()

        if not symptoms:
            QMessageBox.warning(self, "Error", "Selecciona síntomas")
            return

        self.controller.set_symptoms(symptoms, obs)
        self.controller.model.mode = mode
        self.controller.diagnose()



    # ---------------- TEMAS ----------------
    def toggle_dark_mode(self):
        if self.dark_mode_toggle.isChecked():
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def apply_light_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                color: #222;
                font-family: Segoe UI;
                font-size: 14px;
            }
            QGroupBox {
                border: 1px solid #ccc;
                border-radius: 8px;
                margin-top: 10px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
            QListWidget {
                background: white;
                border-radius: 6px;
            }
        """)

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ddd;
                font-family: Segoe UI;
                font-size: 14px;
            }
            QGroupBox {
                border: 1px solid #444;
                border-radius: 8px;
                margin-top: 10px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #0a84ff;
                color: white;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #006edc;
            }
            QListWidget {
                background: #2a2a2a;
                border-radius: 6px;
            }
        """)