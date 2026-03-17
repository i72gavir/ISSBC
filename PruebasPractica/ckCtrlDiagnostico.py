#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:03:26 2026

@author: rgalan
"""

import ckVtsDiagnostico


class ControladorMedico:
    def __init__(self, modelo):
        self.modelo = modelo

    def evaluar(self, sintomas, temperatura):
        resultados = self.modelo.evaluar(sintomas, temperatura)

        self.ventana_resultados = ckVtsDiagnostico.VistaResultados(resultados)
        self.ventana_resultados.show()

            
        
        