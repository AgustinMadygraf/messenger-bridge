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
        "Orquesta el envío de mensaje usando el caso de uso y el gateway inyectado."
        message_body = content_variables.get('body', '')
        message = WhatsappMessage(to=to, body=message_body)
        return send_whatsapp_message_use_case(self.gateway, message, content_sid, content_variables)
