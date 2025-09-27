"""
Path: src/interface_adapter/presenters/gemini_presenter.py
"""

class GeminiPresenter:
    "Presenter para formatear la respuesta del caso de uso antes de mostrarla al usuario."
    def present(self, response):
        "Formatea la respuesta para su presentación."
        return f"Bot: {response}"
