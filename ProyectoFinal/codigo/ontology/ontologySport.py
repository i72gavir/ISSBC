# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:03:34 2026

@author: rgalan
"""

class Sport:
    def __init__(self, name):
        self.name = name


class BodyPart:
    def __init__(self, name):
        self.name = name


class Mechanism:
    def __init__(self, name):
        self.name = name


class Injury:
    def __init__(self, name, base_score=0.5):
        self.name = name
        self.base_score = base_score
        
        
        
class OntologyRule:
    def __init__(self, sport, body_part, mechanism, injury, weight=1.0):
        self.sport = sport
        self.body_part = body_part
        self.mechanism = mechanism
        self.injury = injury
        self.weight = weight



class SportsInjuryOntology:

    def __init__(self):
        self.rules = []
        self._build_ontology()

    def _build_ontology(self):

        # --------------------------
        # RUNNING
        # --------------------------
        self.rules.append(
            OntologyRule(
                sport="Correr",
                body_part="Rodilla",
                mechanism="Sobrecarga",
                injury="Síndrome de la cintilla iliotibial",
                weight=0.95
            )
        )

        self.rules.append(
            OntologyRule(
                sport="Correr",
                body_part="Tobillo",
                mechanism="Torsión",
                injury="Esguince lateral de tobillo",
                weight=0.9
            )
        )

        self.rules.append(
            OntologyRule(
                sport="Correr",
                body_part="Tobillo",
                mechanism="Sobrecarga",
                injury="Tendinitis aquílea",
                weight=0.85
            )
        )

        # --------------------------
        # FOOTBALL
        # --------------------------
        self.rules.append(
            OntologyRule(
                sport="Fútbol",
                body_part="Muslo (cuádriceps)",
                mechanism="Sobrecarga",
                injury="Rotura fibrilar de cuádriceps",
                weight=0.9
            )
        )

        self.rules.append(
            OntologyRule(
                sport="Fútbol",
                body_part="Tobillo",
                mechanism="Torsión",
                injury="Esguince de tobillo",
                weight=0.9
            )
        )

        # --------------------------
        # GYM
        # --------------------------
        self.rules.append(
            OntologyRule(
                sport="Gimnasio - Pesas",
                body_part="Hombro",
                mechanism="Sobrecarga",
                injury="Tendinitis del manguito rotador",
                weight=0.85
            )
        )

        self.rules.append(
            OntologyRule(
                sport="Gimnasio - Pesas",
                body_part="Zona lumbar",
                mechanism="Sobrecarga",
                injury="Lumbalgia mecánica",
                weight=0.8
            )
        )

        # --------------------------
        # STRETCHING
        # --------------------------
        self.rules.append(
            OntologyRule(
                sport="Estiramientos",
                body_part="Muslo (cuádriceps)",
                mechanism="Sobrestiramiento",
                injury="Microlesión muscular",
                weight=0.7
            )
        )

    # --------------------------
    # MOTOR DE INFERENCIA
    # --------------------------
    def infer(self, sport, body_part, symptoms):
        results = []

        for rule in self.rules:

            # --------------------------
            # MATCH FLEXIBLE (NO EXACTO)
            # --------------------------
            sport_match = rule.sport.lower() == sport.lower()
            body_match = rule.body_part.lower() == body_part.lower()
    
            if not sport_match and not body_match:
                continue

            # --------------------------
            # SCORE BASE
            # --------------------------
            score = rule.weight
    
            # --------------------------
            # PESO DE SÍNTOMAS
            # --------------------------
            symptom_weights = {
                "Dolor agudo repentino": 0.15,
                "Inflamación": 0.12,
                "Sensación de chasquido": 0.2,
                "Inestabilidad articular": 0.18,
                "Dolor al apoyar peso": 0.1,
                "Rigidez": 0.08,
                "Fatiga": 0.05
            }

            for s in symptoms:
                score += symptom_weights.get(s, 0.02)

            # --------------------------
            # PENALIZACIÓN DE MISMATCH
            # --------------------------
            mismatch_penalty = 0.2
    
            if not sport_match:
                score -= mismatch_penalty * 0.5
    
            if not body_match:
                score -= mismatch_penalty * 0.7

            # --------------------------
            # CLAMP FINAL
            # --------------------------
            score = max(0.0, min(score, 0.95))
    
            results.append({
                "name": rule.injury,
                "score": round(score, 3)
            })

        # --------------------------
        # NORMALIZACIÓN FINAL
        # --------------------------
        if not results:
            return []
    
        max_score = max(r["score"] for r in results)

        for r in results:
            r["score"] = round(
                r["score"] / (max_score + 1e-6) * 0.95,
                3
            )

        return sorted(results, key=lambda x: x["score"], reverse=True)
        
