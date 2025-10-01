"""
Path: set_telegram_webhook.py
"""

import requests

from src.shared.config import get_config
from src.shared.logger import get_logger

logger = get_logger("set-telegram-webhook")

def set_telegram_webhook():
    "Configura el webhook de Telegram usando la URL pública de ngrok."
    config = get_config()
    telegram_api_key = config.get("TELEGRAM_API_KEY")
    if not telegram_api_key:
        logger.error("TELEGRAM_API_KEY no está configurado en las variables de entorno.")
        return

    # Usa el dominio personalizado si está configurado
    ngrok_domain = config.get("NGROK_DOMAIN")
    if not ngrok_domain:
        logger.error("NGROK_DOMAIN no está configurado en las variables de entorno.")
        return

    webhook_url = f"https://{ngrok_domain}/telegram/webhook"
    set_webhook_url = f"https://api.telegram.org/bot{telegram_api_key}/setWebhook?url={webhook_url}"

    response = requests.get(set_webhook_url, timeout=25)
    if response.status_code == 200:
        logger.info("Webhook de Telegram configurado correctamente: %s", webhook_url)
    else:
        logger.error("Error al configurar el webhook de Telegram: %s", response.text)

if __name__ == "__main__":
    set_telegram_webhook()
