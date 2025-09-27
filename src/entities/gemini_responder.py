"""
Path: src/entities/gemini_responder.py
"""

class GeminiResponder:
    "Abstracción para servicios que generan respuestas a partir de un prompt."
    def get_response(self, _prompt):
        " Genera una respuesta a partir del prompt dado."
        raise NotImplementedError("Debe implementar get_response(prompt)")
