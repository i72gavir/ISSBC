#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  26 16:02:08 2026

Programa para probar los conocimientos obtenidos
durante el desarrollo de la práctica.

@author: Rafa
"""


import sys
from PyQt5.QtWidgets import (QApplication,QPushButton,QToolTip,QMessageBox,QDesktopWidget,
 QMainWindow,QAction,qApp,QMenu,QDialog)
from PyQt5.QtGui import QIcon,QFont


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.state = 0
        self.setWindowTitle('Prueba')
        self.setWindowIcon(QIcon('logo.png'))
        self.setGeometry(300, 300, 300, 220)
        
        
        self.menu()
        self.button()
        self.button2()
        self.button3()
        self.toolbar()
        self.center()
        self.show()
     
    def abrir_ventana(self):
       
        ventana_secundaria = QDialog()
        ventana_secundaria.setWindowTitle('Nueva ventana')
        ventana_secundaria.setWindowIcon(QIcon('logo.png'))
        ventana_secundaria.setGeometry(400, 200, 300, 320)
        ventana_secundaria.exec_()


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
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&Menu")
        
        exitAct = QAction(QIcon("exit.png"), "&Salir", self)
        exitAct.setStatusTip("Cerrar Aplicacion")
        exitAct.triggered.connect(qApp.quit)
        
        groupMenu = QMenu("Ventana",self)
        
        newWindow = QAction(QIcon("vent.png"),"&Nueva ventana",self)
        newWindow.setShortcut("Ctrl+N")
        newWindow.setStatusTip("Abrir una ventana nueva")
        newWindow.triggered.connect(self.abrir_ventana)
        
        groupMenu.addAction(newWindow)
        
        fileMenu.addAction(exitAct)
        fileMenu.addMenu(groupMenu)
        
        
        self.statusBar()


    def contextMenuEvent(self, event):
        cmenu = QMenu(self)
        openAct = cmenu.addAction("Abrir ventana")
        quitAct = cmenu.addAction("Cerrar")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAct:
            qApp.quit()
        elif action == openAct:
            self.abrir_ventana()
            
            
    def toolbar(self):
        exitAct = QAction(QIcon("exit.png"), "Salir", self)
        exitAct.triggered.connect(qApp.quit)
        self.toolbar = self.addToolBar("Salir")
        self.toolbar.addAction(exitAct)            
            

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