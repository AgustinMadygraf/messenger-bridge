"""
Path: run.py
Main entry point for the Twilio bot application.
Supports two modes: CLI for testing and Twilio webhook for production.
"""

import argparse
import sys

from src.shared.logger import get_logger

logger = get_logger("twilio-bot.run")

def run_cli_mode_entry():
    "Runs the application in CLI mode for testing conversations."
    from src.infrastructure.cli.cli_service import run_cli_mode
    logger.info("[CLI] Iniciando modo respuesta...")
    run_cli_mode()

def run_twilio_entry():
    "Runs the application in Twilio webhook mode, only if ngrok starts successfully."
    from src.infrastructure.pyngrok.ngrok_service import NgrokService
    from src.infrastructure.flask.flask_webhook import run_flask_webhook
    logger.info("[Twilio] Iniciando ngrok...")
    ngrok_service = NgrokService(port=5000)
    public_url = ngrok_service.start()
    if not public_url:
        logger.error("No se pudo iniciar ngrok. Twilio no se iniciará.")
        return
    logger.info(f"[Twilio] ngrok iniciado en {public_url}. Iniciando webhook Flask...")
    run_flask_webhook()

def run_telegram_entry():
    "Runs the application in Telegram bot mode."
    from src.infrastructure.telegram_bot.telegram_app import run_telegram_mode
    logger.info("[Telegram] Iniciando modo bot de Telegram...")
    run_telegram_mode()

def main():
    "Main entry point for the application."
    parser = argparse.ArgumentParser(description="Enviar mensaje WhatsApp por Twilio, Telegram o CLI")
    parser.add_argument('--cli', action='store_true', help='Simular recepción y respuesta de mensajes por CLI')
    parser.add_argument('--twilio', action='store_true', help='Recibir y responder mensajes reales por Twilio (webhook)')
    parser.add_argument('--telegram', action='store_true', help='Iniciar el bot de Telegram')
    args = parser.parse_args()

    # Check if a valid mode was specified
    if args.cli:
        run_cli_mode_entry()
    elif args.twilio:
        run_twilio_entry()
    elif args.telegram:
        run_telegram_entry()
    else:
        logger.error("Debe especificar --twilio, --cli o --telegram")
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
