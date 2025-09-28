"""
Path: src/interface_adapter/gateways/twilio_gateway.py
"""

from src.entities.message import Message

class TwilioGateway:
    "Puente para enviar mensajes usando Twilio."
    def __init__(self, sender, from_number):
        self.sender = sender
        self.from_number = from_number

    def send_message(self, message: Message, content_sid: str = "", content_variables: dict = None):
        "Envía un mensaje de WhatsApp usando el sender inyectado."
        return self.sender.send_message(message, content_sid, content_variables)
