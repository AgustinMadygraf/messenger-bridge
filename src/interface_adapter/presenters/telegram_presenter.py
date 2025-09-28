"""
Path: src/interface_adapter/presenters/telegram_presenter.py
"""

from src.entities.message import Message

class TelegramMessagePresenter:
    "Presenter para formatear mensajes de Telegram."
    def build_message(self, chat_id, text):
        "Construye un objeto Message desde el chat_id y el texto."
        return Message(to=chat_id, body=text)

    def present(self, chat_id, response_text):
        "Presenta la respuesta formateada."
        return chat_id, response_text