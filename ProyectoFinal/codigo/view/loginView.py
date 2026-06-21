# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:03:34 2026

@author: rgalan
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Médico")

        layout = QVBoxLayout()

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Acceder")
        self.btn_login.clicked.connect(self.check_login)

        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)
        self.success = False

    def check_login(self):
        if self.user_input.text() == "medico" and self.pass_input.text() == "1234":
            self.success = True
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Credenciales incorrectas")