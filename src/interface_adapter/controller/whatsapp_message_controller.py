"""
Path: src/interface_adapter/controller/whatsapp_message_controller.py
"""


from src.use_cases.send_whatsapp_message_use_case import send_whatsapp_message_use_case
from src.entities.whatsapp_message import WhatsappMessage

class WhatsappMessageController:
    "Controlador para el envío de mensajes WhatsApp usando arquitectura limpia."
    def __init__(self, gateway):
        self.gateway = gateway

    def send_message(self, content_sid, content_variables, to):
        """
        Orquesta el envío de mensaje usando el caso de uso y el gateway inyectado.
        Ahora soporta mensajes multimedia si se proporcionan 'media_url' y 'media_type' en content_variables.
        """
        message_body = content_variables.get('body', '')
        media_url = content_variables.get('media_url')
        media_type = content_variables.get('media_type')
        message = WhatsappMessage(
            to=to,
            body=message_body,
            media_url=media_url,
            media_type=media_type
        )
        return send_whatsapp_message_use_case(self.gateway, message, content_sid, content_variables)
