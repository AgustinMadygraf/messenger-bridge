"""
Path: start.py
Inicia Twilio (WhatsApp) y Telegram en paralelo.
"""

import threading

from src.shared.logger import get_logger

from src.infrastructure.flask.flask_webhook import run_flask_webhook
from src.infrastructure.telegram_bot.telegram_app import run_telegram_mode
from src.infrastructure.pyngrok.ngrok_service import NgrokService

logger = get_logger("twilio-bot.start")

def start_twilio():
    "Inicia el webhook de Twilio en un hilo separado, solo si ngrok inicia correctamente."
    logger.info("[Twilio] Iniciando ngrok...")
    ngrok_service = NgrokService(port=5000)
    public_url = ngrok_service.start()
    if not public_url:
        logger.error("No se pudo iniciar ngrok. Twilio no se iniciará.")
        return
    logger.info("[Twilio] ngrok iniciado en %s. Iniciando webhook Flask...", public_url)
    run_flask_webhook()

def start_telegram():
    "Inicia el bot de Telegram en un hilo separado."
    logger.info("[Telegram] Iniciando bot en hilo separado...")
    run_telegram_mode()

def main():
    "Inicia ambos servicios en paralelo."
    twilio_thread = threading.Thread(target=start_twilio, name="TwilioThread", daemon=True)
    telegram_thread = threading.Thread(target=start_telegram, name="TelegramThread", daemon=True)

    twilio_thread.start()
    telegram_thread.start()

    logger.info("Ambos servicios iniciados en paralelo. Presiona Ctrl+C para detener.")

    # Mantén el hilo principal vivo
    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Deteniendo servicios...")

if __name__ == "__main__":
    main()
