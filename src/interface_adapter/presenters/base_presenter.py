"""
Path: src/interface_adapter/presenters/base_presenter.py
"""

from abc import ABC, abstractmethod

from src.entities.message import Message

class BasePresenter(ABC):
    """Clase base para presentadores de mensajes en diferentes plataformas."""

    @abstractmethod
    def present(self, message: Message):
        """Presenta el mensaje en el formato específico de la plataforma."""
        pass

    def format_common_markdown(self, text: str) -> str:
        """
        Detecta formatos comunes como negrita, cursiva, etc.
        y los normaliza para ser convertidos por cada presentador específico.
        """
        # Implementación común que puede ser heredada o sobrescrita
        return text
