"""
Path: run.py
"""

import argparse
import json

from src.shared.config import get_config
from src.shared.logger import get_logger
from src.infrastructure.twilio.twilio_service import TwilioMessageSender
from src.interface_adapter.gateways.cli_gateway import CliGateway
from src.infrastructure.cli.cli_service import CliMessageSender
from src.interface_adapter.gateways.twilio_gateway import TwilioGateway
from src.interface_adapter.controller.whatsapp_message_controller import WhatsappMessageController
from src.interface_adapter.presenters.cli_presenter import CliPresenter

if __name__ == "__main__":
    logger = get_logger("twilio-bot.run")
    parser = argparse.ArgumentParser(description="Enviar mensaje WhatsApp por Twilio o CLI (plantilla)")
    parser.add_argument('--twilio-plantilla', action='store_true', help='Usar Twilio para enviar el mensaje con plantilla')
    parser.add_argument('--cli-plantilla', action='store_true', help='Simular envío de mensaje por CLI con plantilla')
    parser.add_argument('--cli-respuesta', action='store_true', help='Simular recepción y respuesta de mensajes por CLI')
    parser.add_argument('--twilio-respuesta', action='store_true', help='Recibir y responder mensajes reales por Twilio (webhook)')
    args = parser.parse_args()

    config = get_config()
    if args.twilio_plantilla:
        sender = TwilioMessageSender(config["WHATSAPP_FROM"])
        gateway = TwilioGateway(sender, config["WHATSAPP_FROM"])
    elif args.cli_plantilla:
        sender = CliMessageSender()
        gateway = CliGateway(sender)
    elif args.cli_respuesta:
        # Modo CLI respuesta: simula recepción y respuesta
        print("[CLI] Modo respuesta. Escribe un mensaje para simular recepción:")
        user_input = input("Usuario: ")
        SIMULATED_RESPONSE = f"Bot: Recibido tu mensaje '{user_input}'. Esta es una respuesta simulada."
        print(SIMULATED_RESPONSE)
        exit(0)
    elif args.twilio_respuesta:
        # Modo Twilio respuesta: inicia webhook Flask
        from src.infrastructure.flask.flask_webhook import run_flask_webhook
        run_flask_webhook()
        exit(0)
    else:
        logger.error("Debe especificar --twilio-plantilla, --cli-plantilla, --cli-respuesta o --twilio-respuesta")
        exit(1)

    CONTROLLER = WhatsappMessageController(gateway)
    presenter = CliPresenter()

    if CONTROLLER is not None:
        # Convierte content_variables a dict si es string
        content_variables = config["CONTENT_VARIABLES"]
        if isinstance(content_variables, str):
            try:
                content_variables = json.loads(content_variables)
            except json.JSONDecodeError:
                logger.warning("CONTENT_VARIABLES no es JSON válido, usando como body")
                content_variables = {"body": content_variables}
        logger.debug("content_variables antes de enviar al controlador: %s (tipo: %s)", content_variables, type(content_variables))
        result = CONTROLLER.send_message(
            content_sid=config["CONTENT_SID"],
            content_variables=content_variables,
            to=config["WHATSAPP_TO"]
        )
        logger.info(presenter.present(result))
