# -*- coding: utf-8 -*-

import requests

class OllamaService:
    def __init__(self, model="mistral:latest"):
        self.model = model
        self.url = "http://localhost:11434/api/chat"

    def chat(self, messages):
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }

        response = requests.post(self.url, json=payload)

        if response.status_code == 200:
            return response.json()["message"]["content"]
        else:
            return f"Error: {response.text}"