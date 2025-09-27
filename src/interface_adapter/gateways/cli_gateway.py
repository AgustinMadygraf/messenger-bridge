"""
Path: src/interface_adapter/gateways/cli_gateway.py
"""

from src.shared.logger import get_logger

class CliGateway:
    "Simula el envío de mensajes por línea de comandos."
    def __init__(self):
        self.logger = get_logger("twilio-bot.cli_gateway")

    def send_whatsapp_message(self, message, content_sid, content_variables):
        "Simula el envío de un mensaje de WhatsApp."
        self.logger.info(
            "[CLI] Mensaje simulado enviado a %s con cuerpo '%s' con SID %s y variables %s",
            message.to,
            message.body,
            content_sid,
            content_variables
        )
        return "cli-message-simulated"
