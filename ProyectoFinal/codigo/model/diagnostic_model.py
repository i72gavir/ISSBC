#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:03:27 2026

@author: rgalan
"""

class DiagnosticModel:
    def __init__(self):
        # Inputs clínicos
        self.symptoms = []
        self.observables = {}
        
        # Resultados
        self.hypotheses = []
        self.diagnosis = None
        self.confidence = None
        self.justification = ""
        
        # Fuentes
        self.pdfs = []
        self.source_pdf = None
        self.reason = ""
        self.url = None
        self.web_pages = []
        self.web_sources = []
        
        # Contexto procesado (clave para LLMs)
        self.context_chunks = []

        # Modo de ejecución
        self.mode = "LOCAL"  # LOCAL | WEB