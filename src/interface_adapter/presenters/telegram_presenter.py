"""
Path: src/interface_adapter/presenters/telegram_presenter.py
"""

from src.entities.message import Message

class TelegramMessagePresenter:
    "Presenter para formatear mensajes de Telegram con soporte para Markdown V2."
    def present(self, message: Message) -> dict:
        """
        Presenta la respuesta formateada con soporte para Markdown V2.
        Retorna un diccionario compatible con la API de Telegram.
        """
        # Escapar caracteres especiales para Markdown V2
        escaped_text = self._escape_markdown_v2(message.body)

        return {
            "text": escaped_text,
            "parse_mode": "MarkdownV2"
        }

    def _escape_markdown_v2(self, text: str) -> str:
        """
        Escapa caracteres especiales para formato Markdown V2 de Telegram,
        pero permite * (negrita) y _ (cursiva).
        """
        special_chars = ['[', ']', '(', ')', '~', '`', '>', '#', '+', 
                         '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            text = text.replace(char, f"\\{char}")
        return text
