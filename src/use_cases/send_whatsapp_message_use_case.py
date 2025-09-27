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
        pass #pylint: disable=unnecessary-pass

class SendWhatsAppMessageUseCase:
    """Caso de uso para enviar mensajes de WhatsApp."""
    
    def __init__(self, message_sender: MessageSender):
        """
        Inicializa el caso de uso con un sender.
        
        Args:
            message_sender: Implementación de MessageSender que se utilizará
                            para enviar el mensaje.
        """
        self.message_sender = message_sender
        
    def execute(self, message: WhatsappMessage, content_sid: str, content_variables: dict) -> str:
        """
        Ejecuta el caso de uso para enviar un mensaje WhatsApp.
        
        Args:
            message: Entidad WhatsappMessage con la información del mensaje
            content_sid: ID del contenido de Twilio
            content_variables: Variables para el mensaje
            
        Returns:
            str: ID del mensaje enviado o None si hubo error
        """
        return self.message_sender.send_whatsapp_message(message, content_sid, content_variables)

# Mantener función para compatibilidad con código existente
def send_whatsapp_message_use_case(gateway, message: WhatsappMessage, content_sid, content_variables):
    "Envía un mensaje WhatsApp usando el gateway. Deprecated: Use SendWhatsAppMessageUseCase instead."
    use_case = SendWhatsAppMessageUseCase(gateway)
    return use_case.execute(message, content_sid, content_variables)
