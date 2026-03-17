#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:13:13 2026

@author: rgalan
"""

import ckVtsDiagnostico
import ckCtrlDiagnostico
import ckModeloDiagnostico

import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)

    modelo = ckModeloDiagnostico.ModeloMedico()
    controlador = ckCtrlDiagnostico.ControladorMedico(modelo)
    vista = ckVtsDiagnostico.VistaPrincipal(controlador)

    vista.show()
    sys.exit(app.exec_())


 

 
