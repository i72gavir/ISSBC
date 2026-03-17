#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:03:26 2026

@author: rgalan
"""

class DiagnosticController:
    def __init__(self, model, llm_service):
        self.model = model
        self.llm = llm_service
        self.main_window = None
          
    def set_main_window(self, window):
        self.main_window = window

    def set_symptoms(self, symptoms, observables):
        self.model.symptoms = symptoms
        self.model.observables = observables

    def evaluate_hypotheses(self):
        self.model.hypotheses = self.llm.generate_hypotheses(
            self.model.symptoms,
            self.model.observables,
            self.model.mode,
            self.model.pdfs
        )

    def diagnose(self):
        result = self.llm.generate_diagnosis(
            self.model.symptoms,
            self.model.observables,
            self.model.mode,
            self.model.pdfs
        )

        self.model.diagnosis = result["diagnosis"]
        self.model.confidence = result["confidence"]
        self.model.justification = result["justification"]
        self.model.web_sources = result.get("sources", [])
        
        
    # ----------------- VENTANAS -----------------
    
    def show_hypotheses(self):
        from view.hypothesis_window import HypothesisWindow
        self.hw = HypothesisWindow(self.model.hypotheses, self)
        self.hw.exec()

    def show_diagnosis(self):
        from view.diagnosis_window import DiagnosisWindow
        self.dw = DiagnosisWindow(self.model.diagnosis, self.model.confidence)
        self.dw.exec()

    def show_justification(self):
        from view.justification_window import JustificationWindow
        self.jw = JustificationWindow(self.model.justification)
        self.jw.exec()

    def show_pdf_manager(self):
        from view.pdf_manager_window import PDFManagerWindow
        self.pw = PDFManagerWindow(self.model)
        self.pw.exec()

    def show_web_sources(self):
        if self.model.mode != "WEB":
            return
        from view.web_sources_window import WebSourcesWindow
        self.ww = WebSourcesWindow(self.model.web_sources)
        self.ww.exec()