"""
Path: src/interface_adapter/controller/whatsapp_message_controller.py
"""


from src.interface_adapter.gateways.cli_gateway import CliGateway
from src.interface_adapter.gateways.twilio_gateway import TwilioGateway
from src.use_cases.send_whatsapp_message_use_case import send_whatsapp_message_use_case
from src.entities.whatsapp_message import WhatsappMessage

class WhatsappMessageController:
    "Controlador para el envío de mensajes WhatsApp usando arquitectura limpia."
    def __init__(self, cli_gateway: CliGateway, twilio_gateway: TwilioGateway):
        self.cli_gateway = cli_gateway
        self.twilio_gateway = twilio_gateway

    def send_message(self, _from_, content_sid, content_variables, to, use_cli=False):
        "Orquesta el envío de mensaje usando el caso de uso y el gateway adecuado."
        gateway = self.cli_gateway if use_cli else self.twilio_gateway
        message_body = content_variables.get('body', '')
        message = WhatsappMessage(to=to, body=message_body)
        return send_whatsapp_message_use_case(gateway, message, content_sid, content_variables)
