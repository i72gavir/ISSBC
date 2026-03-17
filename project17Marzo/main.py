#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:13:13 2026

@author: rgalan
"""

import sys
from PyQt5.QtWidgets import QApplication

# Modelo
from model.diagnostic_model import DiagnosticModel

# Controlador
from controller.diagnostic_controller import DiagnosticController

# Servicio LLM (stub)
from services.llm_service import LLMService

# Vista principal
from view.MainView import MainWindow

# Ventanas extra
from view.hipotesisView import HypothesisWindow
from view.diagnosticoView import DiagnosisWindow
from view.justificacionView import JustificationWindow
from view.gestionFilesView import PDFManagerWindow
from view.WebSourcesView import WebSourcesWindow


class AppController(DiagnosticController):
    """
    Extiende el controlador base para añadir navegación entre ventanas
    """

    def __init__(self, model, llm):
        super().__init__(model, llm)
        self.main_window = None

    def set_main_window(self, window):
        self.main_window = window

    # ----------- Navegación UI -----------

    def show_hypotheses(self):
        self.hw = HypothesisWindow(self.model.hypotheses, self)
        self.hw.exec()

    def show_diagnosis(self):
        self.dw = DiagnosisWindow(
            self.model.diagnosis,
            self.model.confidence
        )
        self.dw.exec()

    def show_justification(self):
        if not self.model.justification:
            return
        self.jw = JustificationWindow(self.model.justification)
        self.jw.exec()

    def show_pdf_manager(self):
        self.pw = PDFManagerWindow(self.model)
        self.pw.exec()

    def show_web_sources(self):
        if self.model.mode != "WEB":
            return
        self.ww = WebSourcesWindow(self.model.web_sources)
        self.ww.exec()

def main():
    app = QApplication(sys.argv)

    # ----------- MVC wiring -----------

    model = DiagnosticModel()
    llm_service = LLMService()
    controller = AppController(model, llm_service)

    # Vista principal
    main_window = MainWindow(controller)
    controller.set_main_window(main_window)

    # ----------- Conectar botones extra -----------

    main_window.btn_justify.clicked.connect(controller.show_justification)
    main_window.btn_pdfs.clicked.connect(controller.show_pdf_manager)
    main_window.btn_web.clicked.connect(controller.show_web_sources)

    # ----------- Mostrar app -----------

    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
    
