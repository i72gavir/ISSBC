#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 12:54:49 2026

Ejercicio editor de textos

In this example, we are going to make a text editor than can do differents options:
    open file, save, save as

@author: rgalan
"""


import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QAction, QFileDialog
from pathlib import Path


class TextEditor(QMainWindow):
    
    def __init__(self):
        
        super().__init__()
        self.initUI()

    def initUI(self):
        
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
        self.setWindowTitle("Editor de texto simple")
        self.show()

    def nuevoArchivo(self):
        self.txt.clear()


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


def main():
    app = QApplication(sys.argv)
    ex = TextEditor()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()