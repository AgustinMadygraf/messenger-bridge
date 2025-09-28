"""
Path: src/use_cases/send_whatsapp_message_use_case.py
"""

from abc import ABC, abstractmethod
from src.entities.whatsapp_message import WhatsappMessage

class MessageSender(ABC):
    "Abstracción para enviar mensajes WhatsApp, soportando texto y archivos multimedia."
    @abstractmethod
    def send_whatsapp_message(
        self,
        message: 'WhatsappMessage',
        content_sid: str,
        content_variables: dict
    ) -> str:
        """
        Envía un mensaje WhatsApp.
        Si message.is_media() es True, debe enviar el archivo multimedia usando media_url y media_type.
        Si es False, envía solo texto.
        Args:
            message: WhatsappMessage con texto y/o multimedia.
            content_sid: ID de contenido Twilio.
            content_variables: Variables para el mensaje.
        Returns:
            str: ID del mensaje enviado o None si hubo error.
        """
        pass #pylint: disable=unnecessary-pass

class SendWhatsAppMessageUseCase:
    "Caso de uso para enviar mensajes de WhatsApp, soportando multimedia."
    
    def __init__(self, message_sender: MessageSender):
        self.message_sender = message_sender
        
    def execute(
        self,
        message: WhatsappMessage,
        content_sid: str,
        content_variables: dict
    ) -> str:
        """
        Ejecuta el envío de mensaje WhatsApp (texto o multimedia).
        Args:
            message: WhatsappMessage con texto y/o multimedia.
            content_sid: ID de contenido Twilio.
            content_variables: Variables para el mensaje.
        Returns:
            str: ID del mensaje enviado o None si hubo error.
        """
        return self.message_sender.send_whatsapp_message(message, content_sid, content_variables)

# Mantener función para compatibilidad con código existente
def send_whatsapp_message_use_case(gateway, message: WhatsappMessage, content_sid, content_variables):
    "Envía un mensaje WhatsApp usando el gateway. Deprecated: Use SendWhatsAppMessageUseCase instead."
    use_case = SendWhatsAppMessageUseCase(gateway)
    return use_case.execute(message, content_sid, content_variables)
