"""
Path: start.py
Inicia Twilio (WhatsApp) y Telegram en paralelo usando FastAPI.
"""

from src.shared.logger import get_logger

from src.infrastructure.fastapi.fastapi_webhook import run_fastapi_webhook
from src.infrastructure.pyngrok.ngrok_service import NgrokService

logger = get_logger("twilio-bot.start")

def start_twilio():
    "Inicia el webhook de Twilio en un hilo separado, solo si ngrok inicia correctamente."
    logger.info("[Twilio] Iniciando ngrok...")
    ngrok_service = NgrokService(port=8443)
    public_url = ngrok_service.start()
    if not public_url:
        logger.error("No se pudo iniciar ngrok. Twilio no se iniciará.")
        return
    logger.info("[Twilio] ngrok iniciado en %s. Iniciando webhook FastAPI...", public_url)
    run_fastapi_webhook()

def main():
    "Inicia el servicio FastAPI (Twilio y Telegram webhook) en el hilo principal."
    start_twilio()
    logger.info("Servicio FastAPI iniciado. Presiona Ctrl+C para detener.")

if __name__ == "__main__":
    main()
