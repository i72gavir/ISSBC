# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 17:47:47 2026

@author: Rafa
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QPushButton,
    QFileDialog, QHBoxLayout
)
import os

class PDFManagerWindow(QDialog):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.setWindowTitle("Gestión de PDFs")

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()

        self.btn_add = QPushButton("Añadir")
        self.btn_remove = QPushButton("Eliminar")
        self.btn_clear = QPushButton("Vaciar")

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_remove)
        btn_layout.addWidget(self.btn_clear)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.refresh()

        self.btn_add.clicked.connect(self.add_pdf)
        self.btn_remove.clicked.connect(self.remove_pdf)
        self.btn_clear.clicked.connect(self.clear_pdfs)

    def refresh(self):
        self.list_widget.clear()
        for pdf in self.model.pdfs:
            self.list_widget.addItem(f"{os.path.basename(pdf)}")

    def add_pdf(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar PDFs", "", "PDF Files (*.pdf)")
        self.model.pdfs.extend(files)
        self.refresh()

    def remove_pdf(self):
        for item in self.list_widget.selectedItems():
            self.model.pdfs.remove(item.text())
        self.refresh()

    def clear_pdfs(self):
        self.model.pdfs.clear()
        self.refresh()