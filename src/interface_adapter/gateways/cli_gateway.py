"""
Path: src/infratructure/twilio/cli_gateway.py
"""

class CliGateway:
    "Simula el envío de mensajes por línea de comandos."
    def send_whatsapp_message(self, message, content_sid, content_variables):
        "Simula el envío de un mensaje de WhatsApp."
        print(f"[CLI] Mensaje simulado enviado a {message.to} con cuerpo '{message.body}' con SID {content_sid} y variables {content_variables}")
        return "cli-message-simulated"
