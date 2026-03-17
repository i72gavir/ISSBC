#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:34:22 2026

@author: rgalan
"""

class LLMService:
    """
    Simula un LLM que genera hipótesis y justificación usando PDFs y páginas web.
    """
    def generate_hypotheses(self, symptoms, observables, mode, pdfs, web_pages=[]):
        hypotheses = []

        # Hipótesis base según síntomas frecuentes en medicina deportiva
        if "Fatiga excesiva" in symptoms:
            hypotheses.append({"name": "Sobrecarga muscular", "score": 0.85})
        if "Dolor muscular" in symptoms:
            hypotheses.append({"name": "Contractura muscular", "score": 0.8})
        if "Inflamación" in symptoms:
            hypotheses.append({"name": "Tendinitis", "score": 0.75})
        if "Lesión aguda" in symptoms:
            hypotheses.append({"name": "Distensión muscular", "score": 0.7})

        # Hipótesis derivadas de PDFs
        for pdf in pdfs:
            hypotheses.append({"name": f"Recomendación extraída de {pdf}", "score": 0.6})

        # Hipótesis derivadas de páginas web si modo WEB
        if mode == "WEB":
            for url in web_pages:
                hypotheses.append({"name": f"Información relevante de {url}", "score": 0.5})

        if not hypotheses:
            hypotheses.append({"name": "Evaluación adicional necesaria", "score": 0.5})

        return hypotheses

    def generate_diagnosis(self, symptoms, observables, mode, pdfs, web_pages=[]):
        # Elegir una hipótesis con mayor score como diagnóstico
        hypotheses = self.generate_hypotheses(symptoms, observables, mode, pdfs, web_pages)
        top_hypothesis = max(hypotheses, key=lambda x: x["score"])

        diagnosis = top_hypothesis["name"]
        confidence = top_hypothesis["score"]

        # Justificación combinando síntomas, PDFs y webs
        justification = "Análisis realizado sobre los siguientes datos:\n\n"
        justification += "Síntomas considerados:\n" + "\n".join(symptoms) + "\n\n"

        if pdfs:
            justification += "Información extraída de PDFs:\n"
            for pdf in pdfs:
                justification += f"- {pdf}: fragmento relevante simulado.\n"

        if mode == "WEB" and web_pages:
            justification += "Información obtenida de páginas web:\n"
            for url in web_pages:
                justification += f"- {url}: fragmento relevante simulado.\n"

        # Fragmentos de ejemplo para ventana Fuentes Web
        sources = []
        if mode == "WEB":
            for url in web_pages:
                sources.append({
                    "title": f"Info de {url}",
                    "url": url,
                    "snippet": f"Fragmento relevante extraído de {url}"
                })

        return {
            "diagnosis": diagnosis,
            "confidence": confidence,
            "justification": justification,
            "sources": sources,
            "hypotheses": hypotheses
        }