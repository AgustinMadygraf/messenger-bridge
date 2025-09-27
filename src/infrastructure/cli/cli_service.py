"""
Path: src/infrastructure/cli/cli_service.py
"""

from src.shared.logger import get_logger
from src.use_cases.send_whatsapp_message_use_case import MessageSender

class CliMessageSender(MessageSender):
    "Implementación de MessageSender para CLI con ayuda y feedback de error claro."
    def __init__(self):
        self.logger = get_logger("twilio-bot.cli_service")

    @staticmethod
    def help():
        "Muestra la ayuda de uso para el envío de mensajes por CLI."
        print("""
Uso: python run.py --cli
Simula el envío de un mensaje WhatsApp por CLI.
Argumentos requeridos en config:
  - WHATSAPP_TO: Número de destino
  - CONTENT_SID: SID de contenido
  - CONTENT_VARIABLES: Variables del mensaje
Ejemplo de uso:
  python run.py --cli
""")

    def send_whatsapp_message(self, message, content_sid, content_variables):
        # Validación interactiva de argumentos
        if not message.to:
            print("[ERROR] El número de destino (to) es obligatorio.")
            nuevo_to = input("Ingrese el número de destino (to): ").strip()
            if not nuevo_to:
                print("[ERROR] No se proporcionó un número de destino válido. Abortando.")
                self.help()
                return None
            message.to = nuevo_to
        if not content_sid:
            print("[ERROR] El Content SID es obligatorio.")
            nuevo_sid = input("Ingrese el Content SID: ").strip()
            if not nuevo_sid:
                print("[ERROR] No se proporcionó un Content SID válido. Abortando.")
                self.help()
                return None
            content_sid = nuevo_sid
        if not content_variables or not isinstance(content_variables, dict):
            print("[ERROR] Las variables de contenido son obligatorias y deben ser un diccionario.")
            nuevo_body = input("Ingrese el cuerpo del mensaje (body): ").strip()
            if not nuevo_body:
                print("[ERROR] No se proporcionó un body válido. Abortando.")
                self.help()
                return None
            content_variables = {"body": nuevo_body}
            message.body = nuevo_body
        self.logger.info(
            "[CLI] Mensaje simulado enviado a %s con cuerpo '%s'",
            message.to,
            message.body
        )
        self.logger.info(
            "[CLI] Content SID: %s, Variables: %s",
            content_sid,
            content_variables
        )
        print(f"[OK] Mensaje simulado enviado a {message.to} con cuerpo '{message.body}'")
        return "cli-message-simulated-12345"
