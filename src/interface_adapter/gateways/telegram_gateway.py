"""
Path: src/interface_adapter/gateways/telegram_gateway.py
"""

from src.entities.message import Message

class TelegramGateway:
    "Puente para enviar mensajes usando Telegram."
    def __init__(self, sender):
        self.sender = sender

    def send_message(self, message: Message, _content_sid: str = "", _content_variables: dict = None):
        " Devuelve el texto a enviar. El envío real lo hace el handler."
        if message.is_media():
            return f"{message.body}\n[Multimedia: {message.media_url}]"
        else:
            return message.body

    def add_message_handler(self, handler):
        "Agrega un handler para mensajes entrantes."
        self.sender.add_message_handler(handler)
