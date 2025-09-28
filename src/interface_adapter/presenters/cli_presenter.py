"""
Path: src/interface_adapter/presenters/cli_presenter.py
"""

from src.entities.message import Message

class CliPresenter:
    "Presentador para CLI."
    def present(self, message: Message):
        "Convierte el resultado en un mensaje para mostrar en CLI."
        return f"[CLI] Resultado: {message.body}"
