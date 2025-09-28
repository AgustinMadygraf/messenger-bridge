"""
Path: src/entities/gemini_responder.py
"""

class GeminiResponder:
    "Abstracción para servicios que generan respuestas a partir de un prompt."
    def get_response(self, prompt, system_instructions=None):
        """
        Genera una respuesta a partir del prompt dado y opcionalmente instrucciones de sistema.

        :param prompt: str, el mensaje del usuario.
        :param system_instructions: str | None, instrucciones de sistema para el modelo.
        """
        raise NotImplementedError("Debe implementar get_response(prompt, system_instructions=None)")
