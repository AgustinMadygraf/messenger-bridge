"""
Path: src/interface_adapter/gateways/cli_gateway.py
"""

from src.entities.message import Message

class CliGateway:
    "Puente para simular envío de mensajes por línea de comandos."
    def __init__(self, sender):
        self.sender = sender

    def send_message(self, message: Message, content_sid: str = "", content_variables: dict = None):
        "Simula el envío de un mensaje de WhatsApp usando el sender inyectado."
        return self.sender.send_message(message, content_sid, content_variables)
