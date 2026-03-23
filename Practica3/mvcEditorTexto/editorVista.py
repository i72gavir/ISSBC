# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 17:06:44 2026

@author: rgalan
"""


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QAction, QFileDialog
from PyQt5.QtWidgets import QFontDialog, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QInputDialog, QTextEdit
from PyQt5.QtGui import QKeySequence
from pathlib import Path
from editorControlador import Controlador


class Vista(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.controlador = Controlador()
        self.init_ui()
        

    def init_ui(self):
         
        self.path = None
        self.txt = QTextEdit()
        self.setCentralWidget(self.txt)
        self.statusBar()

        # creamos opcion en el menu
        nuevoArchivo = QAction("Nuevo", self)
        # asignamos atajo
        nuevoArchivo.setShortcut("Ctrl+N")
        nuevoArchivo.setStatusTip("Nuevo archivo")
        nuevoArchivo.triggered.connect(self.nuevoArchivo)

        # creamos opcion en el menu
        abrirFichero = QAction("Abrir", self)
        # asignamos atajo
        abrirFichero.setShortcut("Ctrl+O")
        abrirFichero.setStatusTip("Abrir archivo")
        abrirFichero.triggered.connect(self.abrirArchivo)

        # creamos opcion en el menu
        guardarArchivo = QAction("Guardar", self)
        # asignamos atajo
        guardarArchivo.setShortcut("Ctrl+S")
        guardarArchivo.setStatusTip("Guardar Archivo")
        guardarArchivo.triggered.connect(self.guardarArchivo)

        # creamos opcion en el menu
        guardarComo = QAction("Guardar como", self)
        guardarComo.setStatusTip("Guardar como")
        guardarComo.triggered.connect(self.guardarComo)

        menubar = self.menuBar()
        menuArchivo = menubar.addMenu("&Opciones")
        menuArchivo.addAction(nuevoArchivo)
        menuArchivo.addAction(abrirFichero)
        menuArchivo.addAction(guardarArchivo)
        menuArchivo.addAction(guardarComo)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("Editor de texto MVC")
        self.show()

    def nuevoArchivo(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Crear Archivo", "", "Todos los archivos (*);;Archivos de texto (*.txt)")
        if ruta:
            if self.controlador.crear_archivo(ruta):
                self.text_edit.setPlainText("")
                self.setWindowTitle(f"Editor de Texto MVC- {ruta}")
            else:
                print("Error al crear el archivo")


    def guardarArchivo(self):
        if self.path is None:
            return self.saveAsFile()
        self.save_path()


    def guardarComo(self):
        fname = QFileDialog.getSaveFileName(self, "Guardar archivo")
        if fname[0]:
            f = open(fname[0], "w")
            with f:
                data = self.txt.toPlainText()
                f.write(data)
                f.close()
                self.path = fname
                self.setWindowTitle(fname[0])


    def save_path(self):
        texto = self.txt.toPlainText()
        with open(self.path[0], "w") as f:
            f.write(texto)


    def abrirArchivo(self):
        directorio = str(Path.home())
        nombreArchivo = QFileDialog.getOpenFileName(self, "Abrir archivo", directorio)
        if nombreArchivo[0]:
            f = open(nombreArchivo[0], "r")
            with f:
                data = f.read()
                
                self.txt.setText(data)
                self.path = nombreArchivo
                self.setWindowTitle(nombreArchivo[0])



