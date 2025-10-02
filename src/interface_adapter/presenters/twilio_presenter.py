"""
Path: src/interface_adapter/presenters/twilio_presenter.py
"""

from src.entities.message import Message

class TwilioPresenter:
    "Formatea la respuesta para Twilio (Twiml XML) con soporte para formato básico."
    def present(self, message: Message) -> str:
        """
        Devuelve la respuesta formateada en TwiML.
        Opcionalmente puede convertir algunos formatos markdown a formatos que WhatsApp entienda.
        """
        # Convertir markdown básico a formato WhatsApp (opcional)
        formatted_body = self._convert_to_whatsapp_format(message.body)
        
        # Escape XML para evitar problemas con caracteres especiales
        formatted_body = self._escape_xml(formatted_body)
        
        return f"<Response><Message>{formatted_body}</Message></Response>"
    
    def _convert_to_whatsapp_format(self, text: str) -> str:
        """
        Convierte formato markdown básico a formato WhatsApp
        *texto* se mantiene para negrita
        _texto_ se mantiene para cursiva
        ~texto~ para tachado
        ```texto``` para código
        """
        return text
        
    def _escape_xml(self, text: str) -> str:
        """Escapa caracteres especiales XML"""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
