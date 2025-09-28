"""
Path: run.py
Main entry point for the Twilio bot application.
Supports two modes: CLI for testing and Twilio webhook for production.
"""

import argparse
import sys
from src.shared.logger import get_logger

logger = get_logger("twilio-bot.run")

def run_cli_mode():
    "Runs the application in CLI mode for testing conversations."
    from src.infrastructure.cli.cli_service import setup_cli_mode
    logger.info("[CLI] Iniciando modo respuesta...")
    setup_cli_mode()

def run_twilio_mode():
    "Runs the application in Twilio webhook mode."
    from src.infrastructure.flask.flask_webhook import run_flask_webhook
    logger.info("[Twilio] Iniciando modo webhook...")
    run_flask_webhook()

def main():
    "Main entry point for the application."
    parser = argparse.ArgumentParser(description="Enviar mensaje WhatsApp por Twilio o CLI")
    parser.add_argument('--cli', action='store_true', help='Simular recepción y respuesta de mensajes por CLI')
    parser.add_argument('--twilio', action='store_true', help='Recibir y responder mensajes reales por Twilio (webhook)')
    args = parser.parse_args()

    # Check if a valid mode was specified
    if args.cli:
        run_cli_mode()
    elif args.twilio:
        run_twilio_mode()
    else:
        logger.error("Debe especificar --twilio o --cli")
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
