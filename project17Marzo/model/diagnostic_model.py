#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:03:27 2026

@author: rgalan
"""

class DiagnosticModel:
    def __init__(self):
        self.symptoms = []
        self.observables = {}
        self.hypotheses = []
        self.diagnosis = None
        self.confidence = None
        self.justification = ""
        self.pdfs = []          # PDFs locales
        self.web_pages = []     # URLs añadidas
        self.web_sources = []   # fragmentos relevantes de webs
        self.mode = "LOCAL"     # LOCAL, WEB