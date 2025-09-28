"""
Path: src/interface_adapter/gateways/telegram_gateway.py
"""

from src.entities.message import Message

class TelegramGateway:
    "Puente para enviar mensajes usando Telegram."
    def __init__(self, sender):
        self.sender = sender

    def send_message(self, message: Message, content_sid: str = "", content_variables: dict = None):
        """
        Envía un mensaje usando el sender inyectado.
        Ignora content_sid y content_variables para Telegram.
        """
        import asyncio
        if message.is_media():
            return asyncio.run(self.sender.send_message(message.to, f"{message.body}\n[Multimedia: {message.media_url}]"))
        else:
            return asyncio.run(self.sender.send_message(message.to, message.body))

    def add_message_handler(self, handler):
        "Agrega un handler para mensajes entrantes."
        self.sender.add_message_handler(handler)
