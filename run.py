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
    "Runs the application in Twilio webhook mode (and Telegram webhook), only if ngrok starts successfully."
    from src.infrastructure.pyngrok.ngrok_service import NgrokService
    from src.infrastructure.fastapi.fastapi_webhook import run_fastapi_webhook
    logger.info("[Twilio] Iniciando ngrok...")
    ngrok_service = NgrokService(port=8443)
    public_url = ngrok_service.start()
    if not public_url:
        logger.error("No se pudo iniciar ngrok. Twilio no se iniciará.")
        return
    logger.info("[Twilio] ngrok iniciado en %s. Iniciando webhook FastAPI...", public_url)
    run_fastapi_webhook()  # FastAPI atiende /webhook y /telegram/webhook

def run_telegram_entry():
    "Runs the application in Telegram bot mode (polling only, no webhook server)."
    from src.infrastructure.telegram_bot.telegram_app import run_telegram_mode
    logger.info("[Telegram] Iniciando modo bot de Telegram (polling)...")
    run_telegram_mode()

def main():
    "Main entry point for the application."
    parser = argparse.ArgumentParser(description="Enviar mensaje WhatsApp por Twilio, Telegram o CLI")
    parser.add_argument('--cli', action='store_true', help='Simular recepción y respuesta de mensajes por CLI')
    parser.add_argument('--twilio', action='store_true', help='Recibir y responder mensajes reales por Twilio y Telegram (webhook FastAPI)')
    args = parser.parse_args()

    if args.cli:
        run_cli_mode_entry()
    elif args.twilio:
        run_twilio_entry()
    else:
        logger.error("Debe especificar --twilio o --cli")
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
