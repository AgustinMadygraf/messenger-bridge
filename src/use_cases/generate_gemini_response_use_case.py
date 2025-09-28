"""
Path: src/use_cases/generate_gemini_response_use_case.py
"""

from src.entities.gemini_responder import GeminiResponder

class GenerateGeminiResponseUseCase:
    "Caso de uso para generar una respuesta usando el modelo Gemini."

    def __init__(self, responder):
        if not isinstance(responder, GeminiResponder):
            raise TypeError("El responder debe implementar la interfaz GeminiResponder")
        self.responder = responder

    def execute(self, prompt, system_instructions=None):
        """
        Ejecuta el caso de uso: recibe un prompt y opcionalmente instrucciones de sistema,
        retorna la respuesta generada por Gemini.
        """
        if not prompt or not isinstance(prompt, str):
            raise ValueError("El prompt debe ser un string no vacío.")
        return self.responder.get_response(prompt, system_instructions=system_instructions)
