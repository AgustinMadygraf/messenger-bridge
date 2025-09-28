"""
Path: src/interface_adapter/presenters/telegram_presenter.py
"""

from src.entities.message import Message

class TelegramMessagePresenter:
    "Presenter para formatear mensajes de Telegram."
    def present(self, message: Message):
        "Presenta la respuesta formateada."
        return message.body
