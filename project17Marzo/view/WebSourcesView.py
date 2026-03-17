# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 17:48:07 2026

@author: Rafa
"""

from PyQt5.QtWidgets import ( 
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout
    )
from PyQt5.QtCore import Qt

class WebSourcesWindow(QDialog):
    def __init__(self, sources):
        super(WebSourcesWindow, self).__init__()
        self.setWindowTitle("Fuentes Web")
        self.resize(800, 500)

        layout = QVBoxLayout()

        # Tabla
        self.table = QTableWidget(self)
        self.table.setRowCount(len(sources))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Título", "URL", "Fragmento"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setWordWrap(True)  # Salto de línea

        for i, s in enumerate(sources):
            # Título
            title_item = QTableWidgetItem(s.get("title", ""))
            title_item.setFlags(title_item.flags() ^ Qt.ItemIsEditable)
            title_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            # URL
            url_item = QTableWidgetItem(s.get("url", ""))
            url_item.setFlags(url_item.flags() ^ Qt.ItemIsEditable)
            url_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            # Fragmento
            snippet_item = QTableWidgetItem(s.get("snippet", ""))
            snippet_item.setFlags(snippet_item.flags() ^ Qt.ItemIsEditable)
            snippet_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            self.table.setItem(i, 0, title_item)
            self.table.setItem(i, 1, url_item)
            self.table.setItem(i, 2, snippet_item)

        # Ajuste automático de columnas y filas
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        layout.addWidget(self.table)

        # Botón cerrar
        button_layout = QHBoxLayout()
        self.btn_close = QPushButton("Cerrar")
        button_layout.addStretch()
        button_layout.addWidget(self.btn_close)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Evento del botón cerrar
        self.btn_close.clicked.connect(self.close)