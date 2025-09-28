"""
Path: src/interface_adapter/gateways/telegram_gateway.py
"""

class TelegramGateway:
    "Puente para enviar mensajes usando Telegram."
    def __init__(self, sender):
        self.sender = sender

    async def send_message(self, chat_id, text):
        "Envía un mensaje de texto usando el sender inyectado."
        return await self.sender.send_message(chat_id, text)

    def add_message_handler(self, handler):
        "Agrega un handler para mensajes entrantes."
        self.sender.add_message_handler(handler)
