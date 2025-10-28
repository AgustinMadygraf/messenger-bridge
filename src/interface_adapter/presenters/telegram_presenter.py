"""
Path: src/interface_adapter/presenters/telegram_presenter.py
"""

from src.shared.logger import get_logger

from src.interface_adapter.presenters.markdown_converter import MarkdownConverter
from src.interface_adapter.presenters.markdown_validator import MarkdownValidator
from src.interface_adapter.presenters.message_splitter import MessageSplitter
from src.entities.message import Message

logger = get_logger("telegram-presenter")

class TelegramMessagePresenter:
    "Presenter para formatear mensajes de Telegram con soporte para Markdown V2."
    def __init__(self):
        self.converter = MarkdownConverter()
        self.validator = MarkdownValidator()
        self.splitter = MessageSplitter()

    def present(self, message: Message) -> list:
        "Presenta la respuesta escapando correctamente para MarkdownV2."
        # Limita la longitud de los textos logueados
        telegram_format = self.converter.convert(message.body)
        parts = self.splitter.split(telegram_format, 4096)
        result = []
        error_logged = False
        for part in parts:
            try:
                self.validator.validate(part)
                result.append({
                    "text": part,
                    "parse_mode": "MarkdownV2"
                })
            except ValueError as e:
                if not error_logged:
                    logger.error("MarkdownV2 desbalanceado: %s", e)
                    error_logged = True
                # Devuelve el texto sin formato si está desbalanceado
                result.append({
                    "text": part.replace("*", "").replace("_", ""),
                    "parse_mode": None
                })
        return result
