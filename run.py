"""
Path: start.py
Inicia Twilio (WhatsApp) y Telegram en paralelo usando FastAPI.
"""

import sys
from src.shared.logger import get_logger

from src.infrastructure.fastapi.fastapi_webhook import run_fastapi_webhook
from src.infrastructure.pyngrok.ngrok_service import NgrokService

logger = get_logger("twilio-bot.start")

def start_twilio():
    "Inicia el webhook de Twilio en un hilo separado, solo si ngrok inicia correctamente."
    print("\n---- Iniciando Messenger Bridge ----\n")
    logger.info("[Twilio] Iniciando ngrok...")
    ngrok_service = NgrokService(port=8443)
    public_url = ngrok_service.start()
    if not public_url:
        logger.error("No se pudo iniciar ngrok. Twilio no se iniciará.")
        print("\nContinuando sin soporte de Twilio/WhatsApp...\n")

        # Ask if user wants to continue without ngrok
        if "--no-prompt" not in sys.argv:
            response = input("¿Desea continuar sin el túnel ngrok? (s/N): ").lower()
            if response != 's' and response != 'si' and response != 'sí':
                print("Saliendo...")
                sys.exit(1)
        return

    logger.info("[Twilio] ngrok iniciado en %s. Iniciando webhook FastAPI...", public_url)
    print(f"\n✅ Webhook disponible en: {public_url}\n")
    run_fastapi_webhook()

def main():
    "Inicia el servicio FastAPI (Twilio y Telegram webhook) en el hilo principal."
    start_twilio()
    logger.info("Servicio FastAPI iniciado. Presiona Ctrl+C para detener.")
    print("\n---- Messenger Bridge está ejecutándose ----")
    print("* Presiona Ctrl+C para detener el servicio")

if __name__ == "__main__":
    main()
