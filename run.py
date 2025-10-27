"""
Path: start.py
Inicia Twilio (WhatsApp) y Telegram en paralelo usando FastAPI.
"""



import argparse
import os
import time
import threading
from src.shared.logger import get_logger

from src.infrastructure.fastapi.fastapi_webhook import run_fastapi_webhook
from src.infrastructure.pyngrok.ngrok_service import NgrokService

ngrok_service_instance = None  # Instancia global

def configure_log_level_from_args():
    "Configura el nivel de log desde los argumentos de línea de comandos."
    parser = argparse.ArgumentParser(description="Inicia Twilio (WhatsApp) y Telegram en paralelo usando FastAPI.")
    parser.add_argument("--verbose", action="store_true", help="Muestra todos los mensajes de log (DEBUG)")
    parser.add_argument("--quiet", action="store_true", help="Muestra solo errores y advertencias")
    args, _ = parser.parse_known_args()
    if args.verbose:
        os.environ["LOG_LEVEL"] = "DEBUG"
    elif args.quiet:
        os.environ["LOG_LEVEL"] = "WARNING"
    return args

configure_log_level_from_args()
logger = get_logger("twilio-bot.start")

def print_separator():
    "Imprime un separador en la consola."
    print("\n" + "─" * 40)

def start_ngrok_service(port, endpoints, times):
    global ngrok_service_instance
    logger.info("[Twilio] Iniciando ngrok...")
    t_ngrok_start = time.time()
    ngrok_service_instance = NgrokService(port=port)
    public_url = ngrok_service_instance.start()
    t_ngrok_end = time.time()
    times["Twilio/ngrok"] = t_ngrok_end - t_ngrok_start
    if not public_url:
        # Mensaje de error resaltado y sugerencias agrupadas
        print("\n\033[91m[ERROR] No se pudo iniciar ngrok. Twilio no se iniciará.\033[0m")
        print("    Sugerencias:")
        print("      1. Verifica tu conexión a internet.")
        print("      2. Revisa tu token y configuración de ngrok.")
        print("      3. Consulta la documentación: https://dashboard.ngrok.com/docs")
        print("      4. Ejecuta el script con --verbose para más detalles.")
        endpoints["Twilio"] = None
    else:
        logger.info("[Twilio] ngrok iniciado en %s.", public_url)
        endpoints["Twilio"] = public_url
        endpoints["Telegram"] = f"{public_url}/telegram/webhook"

def start_fastapi_service(times):
    t_fastapi_start = time.time()
    run_fastapi_webhook()
    t_fastapi_end = time.time()
    times["FastAPI"] = t_fastapi_end - t_fastapi_start

def start_twilio():
    "Inicia el webhook de Twilio y FastAPI, FastAPI en el hilo principal y ngrok en un hilo separado."
    print_separator()
    print("🚀 Iniciando Messenger Bridge")
    print_separator()
    endpoints = {}
    times = {}
    port = 8443

    # Lanzar ngrok en un hilo
    ngrok_thread = threading.Thread(target=start_ngrok_service, args=(port, endpoints, times))
    ngrok_thread.start()

    # Ejecutar FastAPI en el hilo principal
    t_fastapi_start = time.time()
    run_fastapi_webhook()
    t_fastapi_end = time.time()
    times["FastAPI"] = t_fastapi_end - t_fastapi_start

    ngrok_thread.join()
    endpoints["FastAPI"] = f"http://0.0.0.0:{port}/webhook"
    return endpoints, times

def main():
    "Inicia el servicio FastAPI (Twilio y Telegram webhook) en el hilo principal."
    t_total_start = time.time()
    try:
        endpoints, times = start_twilio()
        t_total_end = time.time()
        logger.info("Servicio FastAPI iniciado. Presiona Ctrl+C para detener.")
        print_separator()
        print("🟢 Messenger Bridge está ejecutándose")
        print("* Presiona Ctrl+C para detener el servicio")
        print_separator()
        print("Resumen de endpoints activos:")
        for name, url in endpoints.items():
            if url:
                print(f"  - {name}: {url}")
            else:
                print(f"  - {name}: \033[91m⚠️ No disponible\033[0m")
        print_separator()
        print(f"⏱️ Tiempo de arranque total: {t_total_end - t_total_start:.2f} segundos")
        for service, secs in times.items():
            print(f"  - {service}: {secs:.2f} s")
        print_separator()
        # Ya no es necesario el bucle infinito, FastAPI mantiene el proceso vivo
    except KeyboardInterrupt:
        print("\nDeteniendo servicios...")
        if ngrok_service_instance:
            ngrok_service_instance.stop()
        print("Messenger Bridge detenido correctamente.")

if __name__ == "__main__":
    main()
