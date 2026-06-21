#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:13:13 2026

@author: rgalan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication

# Modelo
from model.diagnostic_model import DiagnosticModel

# Controller (ÚNICO)
from controller.diagnostic_controller import DiagnosticController

# Servicio LLM
from services.llm_service import LLMService

# Vista principal
from view.MainView import MainWindow


import controller.diagnostic_controller as dc


def main():
    app = QApplication(sys.argv)

    # ----------- MVC wiring -----------

    model = DiagnosticModel()
    llm_service = LLMService()

    # controller
    controller = DiagnosticController(model, llm_service)

    # Vista principal
    main_window = MainWindow(controller)
    controller.set_main_window(main_window)

    # ----------- Conexiones extra -----------

    main_window.btn_justify.clicked.connect(controller.show_justification)
    main_window.btn_pdfs.clicked.connect(controller.show_pdf_manager)
    main_window.btn_web.clicked.connect(controller.show_web_sources)
    main_window.btn_login.clicked.connect(controller.open_login)

    # ----------- Mostrar app -----------

    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
    
