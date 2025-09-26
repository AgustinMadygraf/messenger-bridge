"""
Path: run.py
"""


import argparse
import json

from src.shared.config import get_config
from src.infrastructure.twilio.twilio_service import TwilioMessageSender
from src.interface_adapter.gateways.cli_gateway import CliGateway
from src.interface_adapter.gateways.twilio_gateway import TwilioGateway
from src.interface_adapter.controller.whatsapp_message_controller import WhatsappMessageController
from src.interface_adapter.presenters.cli_presenter import CliPresenter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enviar mensaje WhatsApp por Twilio o CLI")
    parser.add_argument('--twilio', action='store_true', help='Usar Twilio para enviar el mensaje')
    parser.add_argument('--cli', action='store_true', help='Simular envío de mensaje por CLI')
    args = parser.parse_args()

    config = get_config()
    if args.twilio:
        gateway = TwilioGateway(TwilioMessageSender(config["WHATSAPP_FROM"]), config["WHATSAPP_FROM"])
    elif args.cli:
        gateway = CliGateway()
    else:
        print("Debe especificar --twilio o --cli")
        exit(1)

    # Inicializa solo el gateway necesario
    if args.twilio:
        CONTROLLER = WhatsappMessageController(None, gateway)
    elif args.cli:
        CONTROLLER = WhatsappMessageController(gateway, None)
    else:
        CONTROLLER = None
    presenter = CliPresenter()

    if CONTROLLER is not None:
        # Convierte content_variables a dict si es string
        content_variables = config["CONTENT_VARIABLES"]
        if isinstance(content_variables, str):
            try:
                content_variables = json.loads(content_variables)
            except json.JSONDecodeError:
                content_variables = {"body": content_variables}
        print(f"[DEBUG] content_variables antes de enviar al controlador: {content_variables} (tipo: {type(content_variables)})")
        result = CONTROLLER.send_message(
            _from_=config["WHATSAPP_FROM"],
            content_sid=config["CONTENT_SID"],
            content_variables=content_variables,
            to=config["WHATSAPP_TO"],
            use_cli=args.cli
        )
        print(presenter.present(result))
