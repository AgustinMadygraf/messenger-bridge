"""
Path: set_telegram_webhook.py
"""

import argparse
import os
import requests

from src.shared.config import get_config
from src.shared.logger import get_logger

def configure_log_level_from_args():
    "Configura el nivel de log desde los argumentos de línea de comandos."
    parser = argparse.ArgumentParser(description="Configura el webhook de Telegram usando la URL pública de ngrok.")
    parser.add_argument("--verbose", action="store_true", help="Muestra todos los mensajes de log (DEBUG)")
    parser.add_argument("--quiet", action="store_true", help="Muestra solo errores y advertencias")
    args, _ = parser.parse_known_args()
    if args.verbose:
        os.environ["LOG_LEVEL"] = "DEBUG"
    elif args.quiet:
        os.environ["LOG_LEVEL"] = "WARNING"
    # Si no se especifica, respeta la variable de entorno o config por defecto
    return args

configure_log_level_from_args()
logger = get_logger("set-telegram-webhook")

def set_telegram_webhook():
    "Configura el webhook de Telegram usando la URL pública de ngrok."
    config = get_config()
    telegram_api_key = config.get("TELEGRAM_API_KEY")
    if not telegram_api_key:
        logger.error("TELEGRAM_API_KEY no está configurado en las variables de entorno.")
        return

    # Usa el dominio personalizado si está configurado
    api_domain = config.get("API_DOMAIN")
    if not api_domain:
        logger.error("API_DOMAIN no está configurado en las variables de entorno.")
        return

    # Quita el prefijo https:// si existe
    api_domain = api_domain.replace("https://", "").replace("http://", "")

    webhook_url = f"https://{api_domain}/telegram/webhook"
    set_webhook_url = f"https://api.telegram.org/bot{telegram_api_key}/setWebhook?url={webhook_url}"

    logger.debug("Intentando configurar webhook de Telegram.")
    logger.debug("URL del webhook: %s", webhook_url)
    logger.debug("URL de la petición setWebhook: %s", set_webhook_url)

    response = requests.get(set_webhook_url, timeout=25)
    logger.debug("Respuesta completa de Telegram: %s", response.text)
    if response.status_code == 200:
        logger.info("Webhook de Telegram configurado correctamente: %s", webhook_url)
    else:
        logger.error("Error al configurar el webhook de Telegram: %s", response.text)

if __name__ == "__main__":
    set_telegram_webhook()
