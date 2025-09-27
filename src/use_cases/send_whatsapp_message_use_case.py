"""
Path: src/use_cases/send_whatsapp_message_use_case.py
"""

from abc import ABC, abstractmethod
from src.entities.whatsapp_message import WhatsappMessage

class MessageSender(ABC):
    " Abstracción para enviar mensajes. "
    @abstractmethod
    def send_whatsapp_message(self, message: 'WhatsappMessage', content_sid, content_variables):
        " Envía un mensaje WhatsApp."
        pass # pylint: disable=unnecessary-pass

def send_whatsapp_message_use_case(gateway, message: WhatsappMessage, content_sid, content_variables):
    "Envía un mensaje WhatsApp usando el gateway."
    return gateway.send_whatsapp_message(message, content_sid, content_variables)
