#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:34:22 2026

@author: rgalan
"""

from ontology.ontologySport import SportsInjuryOntology
from services.ollama_service import OllamaService
import json

class LLMService:
    def __init__(self):
        self.ontology = SportsInjuryOntology()
        self.ollama = OllamaService()

    # ---------------------------
    # CONTEXTO
    # ---------------------------
    def _build_context(self, symptoms, observables, pdfs, web_pages):
        context = []

        context.append("SÍNTOMAS: " + ", ".join(symptoms))
        context.append("OBSERVABLES: " + str(observables))

        if pdfs:
            context.append("PDFs: " + ", ".join(pdfs))

        if web_pages:
            context.append("Web: " + ", ".join(web_pages))

        return "\n".join(context)

    # ---------------------------
    # HIPÓTESIS
    # ---------------------------
    ontology = SportsInjuryOntology()

    def generate_hypotheses(self, symptoms, observables, mode, pdfs, web_pages=None):
        if web_pages is None:
            web_pages = []
    
        sport = observables.get("activity")
        body_part = observables.get("body_part")
        
        # INFERENCIA ONTOLÓGICA
        ontology_results = self.ontology.infer(
            sport,
            body_part,
            symptoms
        )
     
        hypotheses = []
     
        # añadir resultados de ontología
        for r in ontology_results:
            hypotheses.append(r)
     
        # fallback si no hay resultados
        if not hypotheses:
            hypotheses.append({
                "name": "Evaluación clínica adicional necesaria",
                "score": 0.5
            })
     
        return hypotheses

    def _build_reason(self, top, symptoms, observables):
        reasons = []

        reasons.append(f"Es la hipótesis con mayor probabilidad ({top.get('score', 0):.2f}).")

        if "Rodilla" in str(observables.get("body_part")):
            reasons.append("Coincide con la zona afectada.")

        if len(symptoms) >= 2:
            reasons.append("Presenta concordancia con múltiples síntomas clínicos.")

        return " ".join(reasons)

    def generate_web_hypotheses(self, symptoms, observables):
        prompt = f"""
            Eres un médico deportivo experto.
            
            Simula que has consultado literatura médica en internet.
            
            Devuelve EXACTAMENTE 3 hipótesis médicas.
            
            Cada una debe tener:
            - name: nombre de la lesión
            - score: probabilidad entre 0 y 1
            - url: fuente médica simulada (ej: pubmed, mayo clinic, etc.)
            
            IMPORTANTE:
            Responde SOLO en JSON válido.
            
            Datos del paciente:
            Síntomas: {symptoms}
            Zona: {observables.get("body_part")}
            Actividad: {observables.get("activity")}
            
            Formato:
            [
              {{"name": "", "score": 0.0, "url": ""}},
              {{"name": "", "score": 0.0, "url": ""}},
              {{"name": "", "score": 0.0, "url": ""}}
            ]
        """
    
        messages = [{"role": "user", "content": prompt}]
        response = self.ollama.chat(messages)
    
        return response


    # ---------------------------
    # DIAGNÓSTICO
    # ---------------------------
    def generate_diagnosis(self, symptoms, observables, mode, pdfs, web_pages=None):
        import random
        if web_pages is None:
            web_pages = []

        if mode == "WEB":
            return self.generate_web_diagnosis(symptoms, observables)

        hypotheses = self.generate_hypotheses(
            symptoms, observables, mode, pdfs, web_pages
        )

        top = max(hypotheses, key=lambda x: x["score"])
        
        justification = self.build_clinical_reason(top, symptoms)
        url = self._select_pdf(pdfs, symptoms)

        return {
            "diagnosis": top["name"],
            "confidence": float(top["score"]),
            "justification": justification,
            "url": url,   # LOCAL no tiene web real
            "hypotheses": hypotheses
        }
    
    def generate_web_diagnosis(self, symptoms, observables):
        raw = self.generate_web_hypotheses(symptoms, observables)
    
        hypotheses = self.parse_web_response(raw)
    
        if not hypotheses:
            return {
                "diagnosis": "Sin datos suficientes",
                "confidence": 0.0,
                "url": None,
                "hypotheses": []
            }
    
        top = max(hypotheses, key=lambda x: x["score"])
    
        return {
            "diagnosis": top["name"],
            "confidence": top["score"],
            "url": top["url"],
            "hypotheses": hypotheses
        }
    
    def _select_pdf(self, pdfs, symptoms):
        if not pdfs:
            return None

        return pdfs[0]
    
    def parse_web_response(self, text):
        try:
            return json.loads(text)
        except:
            return []    
    
    # ---------------------------
    # FUENTES
    # ---------------------------
    def _build_sources(self, mode, web_pages):
        if mode != "WEB":
            return []

        return [
            {
                "title": f"Fuente {url}",
                "url": url,
                "snippet": f"Fragmento simulado de {url}"
            }
            for url in web_pages
        ]

    # ---------------------------
    # JUSTIFICACIÓN
    # ---------------------------
    def _build_context(self, symptoms, observables, pdfs, web_pages):
        return (
            "ANÁLISIS CLÍNICO\n\n"
            f"Síntomas: {', '.join(symptoms)}\n"
            f"Observables: {observables}\n\n"
            f"PDFs: {', '.join(pdfs) if pdfs else 'Ninguno'}\n"
            f"Web: {', '.join(web_pages) if web_pages else 'Ninguno'}"
        )
    
    def build_clinical_reason(self, top, symptoms):
        name = top.get("name", "hipótesis seleccionada")

        # síntomas relevantes
        relevant_symptoms = symptoms[:3]

        symptoms_text = ", ".join(symptoms)

        return (
            f"Se selecciona '{name}' porque presenta compatibilidad con los síntomas "
            f"reportados ({symptoms_text}), los cuales son característicos de esta patología "
            f"según el modelo de inferencia clínica."
        )
    

        

        
        
  