#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:03:26 2026

@author: rgalan
"""

from PyQt5.QtCore import QThread, pyqtSignal
from view.loginView import LoginDialog
from view.medicoView import MedicoView

from services.ollama_service import OllamaService


class DiagnosisWorker(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, model, llm_service):
        super().__init__()
        self.model = model
        self.llm = llm_service

    def run(self):
        # -------------------------
        # MODO WEB
        # -------------------------
        if self.model.mode == "WEB":
           result = self.llm.generate_web_diagnosis(
               self.model.symptoms,
               self.model.observables
           )
    
        # -------------------------
        # MODO LOCAL
        # -------------------------
        else:
           result = self.llm.generate_diagnosis(
               self.model.symptoms,
               self.model.observables,
               self.model.mode,
               self.model.pdfs,
               self.model.web_pages
           )
    
        self.finished.emit(result)

class DiagnosticController:
    def __init__(self, model, llm_service):
        self.model = model
        self.llm = llm_service
        self.main_window = None

        # Ollama
        self.ollama = OllamaService()
        self.chat_history = []

        # estado UI
        self.worker = None
        self._processing_diagnosis = False

        # ventanas
        self._hypothesis_window = None
        self._diagnosis_window = None
        self._just_window = None
        self._pdf_window = None
        self._web_window = None

    def set_main_window(self, window):
        self.main_window = window

    # -------------------------
    # INPUTS
    # -------------------------
    def set_symptoms(self, symptoms, observables):
        self.model.symptoms = symptoms
        self.model.observables = observables

    def set_mode(self, mode):
        self.model.mode = mode

    # -------------------------
    # HIPÓTESIS
    # -------------------------
    def evaluate_hypotheses(self):
        if self.model.mode == "WEB":

            raw = self.llm.generate_web_hypotheses(
                self.model.symptoms,
                self.model.observables
            )
            self.model.hypotheses = self.llm.parse_web_response(raw)

        else:
            self.model.hypotheses = self.llm.generate_hypotheses(
                self.model.symptoms,
                self.model.observables,
                self.model.mode,
                self.model.pdfs,
                self.model.web_pages
            )

        self.show_hypotheses()

    def show_hypotheses(self):
        from view.hipotesisView import HypothesisWindow

        if self._hypothesis_window and self._hypothesis_window.isVisible():
            return

        self._hypothesis_window = HypothesisWindow(
            self.model.hypotheses,
            self
        )
        
        #  cuando se cierre, liberar referencia
        self._hypothesis_window.finished.connect(self._on_hypothesis_closed)
    
        self._hypothesis_window.exec()


    def _on_hypothesis_closed(self):
        self._hypothesis_window = None

    # -------------------------
    # DIAGNÓSTICO
    # -------------------------
    def diagnose(self):
        if self._processing_diagnosis:
            return  # evita doble ejecución
    
        self._processing_diagnosis = True
    
        # Creamos el worker
        self.worker = DiagnosisWorker(self.model, self.llm)
        
        self.worker.finished.connect(self._on_diagnosis_ready)
        self.worker.start()
    
        if self.main_window:
            self.main_window.btn_diagnose.setEnabled(False)
            self.main_window.btn_diagnose.setText("Procesando...")

    def _on_diagnosis_ready(self, result):

        # evitar ejecuciones duplicadas
        if not self._processing_diagnosis:
            return
    
        self._processing_diagnosis = False
    
        if not result or "diagnosis" not in result:
            return
    
        self.model.diagnosis = result.get("diagnosis", "")
        self.model.confidence = result.get("confidence", 0.0)
        self.model.justification = result.get("justification", "")
        self.model.url = result.get("url", None)
        self.model.hypotheses = result.get("hypotheses", [])
        
    
        if self.main_window:
            self.main_window.btn_diagnose.setEnabled(True)
            self.main_window.btn_diagnose.setText("Diagnosticar")
    
        # cerrar ventana anterior si existe
        if self._diagnosis_window and self._diagnosis_window.isVisible():
            self._diagnosis_window.close()
    
        self.show_diagnosis()

    def show_diagnosis(self):
        from view.diagnosticoView import DiagnosisWindow
    
        if not self.model.diagnosis:
            return
    
        # evita doble ventana
        if self._diagnosis_window and self._diagnosis_window.isVisible():
            return
    
        self._diagnosis_window = DiagnosisWindow(
            self.model.diagnosis,
            self.model.confidence,
            self.model.justification,
            self.model.url
        )
    
        self._diagnosis_window.finished.connect(self._on_diag_closed)
    
        self._diagnosis_window.exec()
        
        
    def _on_diag_closed(self):
        self._diagnosis_window = None
        
        
    # -------------------------
    # Justificacion
    # -------------------------
        
    def show_justification(self):    
        from view.justificacionView import JustificationWindow
        self._just_window = JustificationWindow(
            self.model.justification,
            self.model.diagnosis,
            self.model.confidence,
            self.model.url
        )   
        self._just_window.exec()
    
    # -------------------------
    # PDF
    # -------------------------

    def show_pdf_manager(self):
        from view.gestionFilesView import PDFManagerWindow
        self._pdf_window = PDFManagerWindow(self.model)
        self._pdf_window.exec()
    
    # -------------------------
    # WEB SOURCES
    # -------------------------
    def show_web_sources(self):
        from view.WebSourcesView import WebSourcesWindow
        if self.model.mode == "WEB":
            sources = self.model.web_sources or []
            self._web_window = WebSourcesWindow(sources, mode="WEB")
        else:
            self._web_window = WebSourcesWindow(self.model.web_sources or [], mode="LOCAL")

        self._web_window.exec()
            


   # -------------------------
   # LOGIN Y MEDICO
   # -------------------------  
    def send_chat_message(self, user_message):
        system_context = f"""
        Eres un asistente experto en medicina deportiva clínica.

        REGLAS ESTRICTAS:
        - NO des consejos genéricos de bienestar.
        - NO hables de alimentación general, agua o hábitos a menos que estén relacionados con el caso.
        - NO seas un coach de fitness.
        - SOLO responde basado en el contexto médico del paciente.

        CONTEXTO DEL PACIENTE:

        Síntomas:
        {self.model.symptoms}
            
        Observables:
        {self.model.observables}

        Hipótesis:
        {self.model.hypotheses}

        Diagnóstico actual:
        {self.model.diagnosis}
        ({self.model.confidence})

        INSTRUCCIONES DE RESPUESTA:
        - Responde como si fueras un médico deportivo.
        - Justifica siempre con el contexto clínico.
        - Si falta información, di qué falta.
        - Evita recomendaciones genéricas no relacionadas.
        """

        messages = [
            {"role": "system", "content": system_context},
            {"role": "user", "content": user_message + "\nResponde de forma clínica y concreta."}
        ]

        response = self.ollama.chat(messages)

        self.chat_history.append({"role": "user", "content": user_message})
        self.chat_history.append({"role": "assistant", "content": response})

        return response
        
    def open_chat(self):
        from view.chatView import ChatWindow
        self.chat_window = ChatWindow(self)
        self.chat_window.exec()
        
    # -------------------------
    # LOGIN Y MEDICO
    # -------------------------   
        
    def get_current_data(self):
        return {
            "symptoms": self.model.symptoms,
            "observables": self.model.observables,
            "mode": self.model.mode
        }

    def load_data(self, data):
        self.model.symptoms = data.get("symptoms", [])
        self.model.observables = data.get("observables", {})
        
        
    def open_login(self):
        dialog = LoginDialog()

        if dialog.exec_() and dialog.success:
            self.open_medico_view()

    def open_medico_view(self):
        self.medico_view = MedicoView(self)
        self.medico_view.show()
   
        