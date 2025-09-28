"""
Path: src/interface_adapter/presenters/gemini_presenter.py
"""

from src.entities.message import Message

class GeminiPresenter:
    "Presenter para formatear la respuesta del caso de uso antes de mostrarla al usuario."
    def present(self, message: Message):
        "Formatea la respuesta para su presentación."
        return f"Bot: {message.body}"
