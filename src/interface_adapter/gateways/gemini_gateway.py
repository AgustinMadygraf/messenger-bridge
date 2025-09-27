"""
Path: src/interface_adapter/gateways/gemini_gateway.py
"""

from src.entities.gemini_responder import GeminiResponder

class GeminiGateway(GeminiResponder):
    "Gateway para interactuar con el servicio Gemini a través de la interfaz definida."
    def __init__(self, gemini_service):
        self.gemini_service = gemini_service

    def get_response(self, prompt):
        return self.gemini_service.get_response(prompt)
