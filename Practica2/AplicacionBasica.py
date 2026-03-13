# -*- coding: utf-8 -*-
#!/usr/bin/python

"""

Programa para probar los conocimientos obtenidos
durante el desarrollo de la práctica.

Author: rgalan
"""

import sys
from PyQt5.QtWidgets import (QApplication,QPushButton,QToolTip,QMessageBox,QDesktopWidget,
 QMainWindow,QAction,qApp,QMenu,QDialog,QVBoxLayout, QTextEdit,QHBoxLayout,QFileDialog)
from PyQt5.QtGui import QFont


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.state = 0
        self.setWindowTitle('Aplicación básica')
        self.setGeometry(300, 300, 300, 300)
        
        
        self.menu()
        self.button()
        self.button2()
        self.button3()
        self.toolbar()
        self.center()
        self.show()
     
        
    def abrir_ventana(self):
    
        ventana_secundaria = QDialog(self)
        ventana_secundaria.setWindowTitle("Editor de texto")
        ventana_secundaria.resize(400, 350)
    
        layout = QVBoxLayout()
    
        editor = QTextEdit()
        layout.addWidget(editor)
    
        botones = QHBoxLayout()
    
        btn_abrir = QPushButton("Abrir")
        btn_guardar = QPushButton("Guardar")
        btn_guardar_como = QPushButton("Guardar como")
    
        botones.addWidget(btn_abrir)
        botones.addWidget(btn_guardar)
        botones.addWidget(btn_guardar_como)
    
        layout.addLayout(botones)
        ventana_secundaria.setLayout(layout)
    
        ruta = None
    
        def abrir_archivo():
            nonlocal ruta
            ruta_archivo, _ = QFileDialog.getOpenFileName(
                ventana_secundaria,
                "Abrir archivo",
                "",
                "Archivos de texto (*.txt);;Todos los archivos (*)"
            )
    
            if ruta_archivo:
                with open(ruta_archivo, "r", encoding="utf-8") as f:
                    editor.setText(f.read())
                ruta = ruta_archivo
    
        def guardar_archivo():
            nonlocal ruta
            if ruta:
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(editor.toPlainText())
            else:
                guardar_como()
    
        def guardar_como():
            nonlocal ruta
            ruta_archivo, _ = QFileDialog.getSaveFileName(
                ventana_secundaria,
                "Guardar como",
                "",
                "Archivos de texto (*.txt);;Todos los archivos (*)"
            )
    
            if ruta_archivo:
                with open(ruta_archivo, "w", encoding="utf-8") as f:
                    f.write(editor.toPlainText())
                ruta = ruta_archivo
    
        btn_abrir.clicked.connect(abrir_archivo)
        btn_guardar.clicked.connect(guardar_archivo)
        btn_guardar_como.clicked.connect(guardar_como)
    
        ventana_secundaria.exec()
        

    def closeEvent(self, event):
 
        reply = QMessageBox.question(self, 'Cerrar Ventana',"¿Desea salir?", QMessageBox.Yes |QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()   
        
    
    def toggle_button(self):
        if self.state==1:
            self.state=0
            
            self.button.setText('Mostrar grande')
            self.btn.show()
        else:
            self.state=1

            self.button.setText('Mostrar normal')
            self.btn.hide()       

    def button(self):
        #Font and Size
        QToolTip.setFont(QFont('TimesNewRoman', 12))
        
        #Create button
        self.button = QPushButton('Mostrar grande', self)
        
        #Buttton do
        self.button.clicked.connect(self.toggle_button)
        
        #Button extra info
        self.button.setToolTip('Con este boton cambio el tipo')
        
        #Button size
        self.button.resize(self.button.sizeHint())
        self.button.setStyleSheet('background-color: #ff6; color: black;')
        
        self.button.move(50, 50)



    def button2(self):
        # Font and Size
        QToolTip.setFont(QFont('TimesNewRoman', 12))
        
        # Create button
        self.btn = QPushButton('Grande', self)
        
        # Button do
        self.btn.clicked.connect(self.grande)
        
        # Button sizen
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(50, 100)
        

    def button3(self):
        # Font and Size
        QToolTip.setFont(QFont('TimesNewRoman', 12))
        
        # Create button
        self.btn = QPushButton('Normal', self)
        
        # Button do
        self.btn.clicked.connect(self.normal)
        # Button sizen
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(50, 100)

     
    def grande(self):
        self.resize(450, 350)
        self.setWindowTitle('Pantalla mas grande')

    def normal(self):
         reply = QMessageBox.question(self, 'Aviso', "¿Desea hacer la ventana normal?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
         if reply==QMessageBox.Yes:
             self.resize(350, 250)
             self.setWindowTitle('Como estaba')

    def menu(self):
        
            
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&Menu")
        
        exitAct = QAction( "&Salir", self)
        exitAct.setStatusTip("Cerrar Aplicacion")
        exitAct.triggered.connect(qApp.quit)
        
        groupMenu = QMenu("Ventana",self)
        
        newWindow = QAction("&Nueva ventana",self)
        newWindow.setShortcut("Ctrl+N")
        newWindow.setStatusTip("Abrir una ventana nueva")
        newWindow.triggered.connect(self.abrir_ventana)
        

        viewStatAct = QAction('&Barra de estado', self, checkable=True)
        viewStatAct.setStatusTip('Barra de estado')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.toggleMenu)

        
        groupMenu.addAction(newWindow)
        
        fileMenu.addAction(exitAct)
        fileMenu.addMenu(groupMenu)
        fileMenu.addAction(viewStatAct)
        
        
       # self.statusBar()


    def contextMenuEvent(self, event):
        cmenu = QMenu(self)
        openAct = cmenu.addAction("Abrir ventana")
        quitAct = cmenu.addAction("Cerrar")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAct:
            qApp.quit()
        elif action == openAct:
            self.abrir_ventana()
  
    def toggleMenu(self, state):

        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()
            
    def toolbar(self):
        exitAct = QAction("Salir", self)
        exitAct.triggered.connect(qApp.quit)
        self.toolbar = self.addToolBar("Salir")
        self.toolbar.addAction(exitAct)            
        
        newWindow = QAction("&Nueva ventana",self)
        newWindow.triggered.connect(self.abrir_ventana)
        self.toolbar = self.addToolBar("Abrir Ventana")
        self.toolbar.addAction(newWindow)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())    

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()