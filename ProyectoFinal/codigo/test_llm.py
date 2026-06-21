# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 19:41:13 2026

@author: Rafa
"""

# test_llm.py
from services.llm_service import LLMService

# Instanciamos el servicio LLM
services = LLMService()

# Datos de ejemplo
symptoms = ["Fatiga excesiva", "Dolor muscular"]
observables = {"Frecuencia cardíaca": "Alta", "Tensión muscular": "Media"}
pdfs = ["Prevencion_lesiones_deportivas.pdf"]  # simula que tienes este PDF
web_pages = ["https://www.semed.es", "https://archivosdemedicinadeldeporte.com"]

# Generar hipótesis
print("=== HIPÓTESIS ===")
hypotheses = services.generate_hypotheses(symptoms, observables, "WEB", pdfs, web_pages)
for h in hypotheses:
    print(f"{h['name']} - score: {h['score']}")

# Generar diagnóstico final
print("\n=== DIAGNÓSTICO FINAL ===")
diagnosis_data = services.generate_diagnosis(symptoms, observables, "WEB", pdfs, web_pages)
print("Diagnóstico:", diagnosis_data["diagnosis"])
print("Confianza:", diagnosis_data["confidence"])

# Mostrar justificación
print("\n=== JUSTIFICACIÓN ===")
print(diagnosis_data["justification"])

# Mostrar fragmentos de las páginas web (fuentes)
print("\n=== FUENTES WEB ===")
for src in diagnosis_data["sources"]:
    print(f"{src['title']} - {src['url']}")
    print(f"Fragmento: {src['snippet']}\n")