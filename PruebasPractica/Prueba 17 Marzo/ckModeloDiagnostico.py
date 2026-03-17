#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:03:27 2026

@author: rgalan
"""

class ModeloMedico:
    def evaluar(self, sintomas, temperatura):
        resultados = []

        # Reglas simples con puntuación
        score_esguince = 0
        if "dolor" in sintomas: score_esguince += 2
        if "inflamacion" in sintomas: score_esguince += 2
        if "limitacion_movimiento" in sintomas: score_esguince += 1

        score_contractura = 0
        if "rigidez" in sintomas: score_contractura += 2
        if "dolor" in sintomas: score_contractura += 1

        score_tendinitis = 0
        if "dolor" in sintomas: score_tendinitis += 1
        if "dolor_movimiento" in sintomas: score_tendinitis += 2

        score_infeccion = 0
        if temperatura > 37.5: score_infeccion += 3
        if "inflamacion" in sintomas: score_infeccion += 1

        resultados.append(("Esguince", score_esguince))
        resultados.append(("Contractura", score_contractura))
        resultados.append(("Tendinitis", score_tendinitis))
        resultados.append(("Posible infección", score_infeccion))

        # Ordenar por probabilidad (score)
        resultados.sort(key=lambda x: x[1], reverse=True)

        return resultados
