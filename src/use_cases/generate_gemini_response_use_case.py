"""
Path: src/use_cases/generate_gemini_response_use_case.py
"""

from src.infrastructure.google_generativeai.gemini_service import GeminiService

class GenerateGeminiResponseUseCase:
    "Caso de uso para generar una respuesta usando el modelo Gemini."

    def __init__(self, gemini_service=None):
        self.gemini_service = gemini_service or GeminiService()

    def execute(self, prompt):
        "Ejecuta el caso de uso: recibe un prompt y retorna la respuesta generada por Gemini."
        if not prompt or not isinstance(prompt, str):
            raise ValueError("El prompt debe ser un string no vacío.")
        return self.gemini_service.get_response(prompt)
