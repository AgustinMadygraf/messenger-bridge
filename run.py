"""
Path: start.py
"""

import argparse
import os
import time
import threading

from src.shared.logger import get_logger

from src.infrastructure.fastapi.fastapi_webhook import run_fastapi_webhook
from src.infrastructure.pyngrok.ngrok_service import NgrokService

ngrok_service_instance = None

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
    print("\033[96m" + "─" * 40 + "\033[0m")

def start_ngrok_service(port, endpoints, times):
    "Inicia el servicio ngrok y actualiza los endpoints."
    logger.info("[Twilio] Iniciando ngrok...")
    t_ngrok_start = time.time()
    local_ngrok_service_instance = NgrokService(port=port)
    public_url = local_ngrok_service_instance.start()
    t_ngrok_end = time.time()
    times["Twilio/ngrok"] = t_ngrok_end - t_ngrok_start
    if not public_url:
        logger.error("No se pudo iniciar ngrok. Twilio no se iniciará.")
        logger.warning("Sugerencias para resolver el problema:")
        logger.warning("  1. Verifica tu conexión a internet y que ngrok esté instalado correctamente.")
        logger.warning("  2. Revisa tu token y configuración de ngrok en el archivo .env o config.py.")
        logger.warning("  3. Consulta la documentación oficial: https://dashboard.ngrok.com/docs")
        logger.warning("  4. Ejecuta el script con --verbose para ver detalles técnicos.")
        logger.warning("  5. Si el error persiste, ejecuta: python set_telegram_webhook.py --check-ngrok")
        logger.warning("  6. Para soporte rápido, contacta: support@example.com")
        respuesta = input("¿Deseas reintentar iniciar ngrok? (S/N): ").strip().lower()
        if respuesta == "s":
            logger.info("Reintentando iniciar ngrok...")
            public_url = local_ngrok_service_instance.start()
            if public_url:
                logger.info("[Twilio] ngrok iniciado en %s.", public_url)
                endpoints["Twilio"] = public_url
                endpoints["Telegram"] = f"{public_url}/telegram/webhook"
                print("\033[92m✔️ ngrok iniciado correctamente tras reintento.\033[0m")
            else:
                print("\033[91m❌ ngrok sigue sin iniciar. Revisa la configuración y vuelve a intentarlo.\033[0m")
                endpoints["Twilio"] = None
        else:
            endpoints["Twilio"] = None
    else:
        logger.info("[Twilio] ngrok iniciado en %s.", public_url)
        endpoints["Twilio"] = public_url
        endpoints["Telegram"] = f"{public_url}/telegram/webhook"
    return local_ngrok_service_instance

def start_fastapi_service(times):
    "Inicia el webhook de FastAPI."
    t_fastapi_start = time.time()
    run_fastapi_webhook()
    t_fastapi_end = time.time()
    times["FastAPI"] = t_fastapi_end - t_fastapi_start

def start_twilio():
    "Inicia el webhook de Twilio y FastAPI, FastAPI en un hilo separado y ngrok en otro."
    endpoints = {}
    times = {}
    port = 8443

    # Lanzar ngrok en un hilo
    ngrok_thread = threading.Thread(target=start_ngrok_service, args=(port, endpoints, times))
    ngrok_thread.start()

    # Lanzar FastAPI en un hilo
    fastapi_thread = threading.Thread(target=start_fastapi_service, args=(times,))
    fastapi_thread.start()

    # Esperar a que ngrok esté listo
    ngrok_thread.join()
    endpoints["FastAPI"] = f"http://0.0.0.0:{port}/webhook"


    # El hilo principal queda bloqueado por FastAPI
    fastapi_thread.join()
    return endpoints, times

def print_summary(endpoints, times, t_total_start):
    "Imprime un resumen de los endpoints y tiempos de arranque."
    print_separator()
    print("🚀 Messenger Bridge v1.2.0")
    print("Bienvenido! Documentación: docs/installation.md | Soporte: support@example.com")
    print("🟢 Messenger Bridge ejecutándose | Ctrl+C para detener")
    print_separator()
    print("Endpoints activos:")
    for name, url in endpoints.items():
        if url:
            print(f"  - {name}: {url}")
        else:
            print(f"  - {name}: \033[91m⚠️ No disponible\033[0m")
    print_separator()
    print(f"⏱️ Arranque: {time.time() - t_total_start:.2f}s")
    for service, secs in times.items():
        print(f"  - {service}: {secs:.2f} s")
    print_separator()
    print("💡 Envía un mensaje por Telegram para probar la integración.")

def main():
    "Función principal para iniciar Twilio (WhatsApp) y Telegram en paralelo usando FastAPI."
    t_total_start = time.time()
    endpoints = {}
    times = {}
    port = 8443

    ngrok_service_instance_holder = {}

    # Lanzar ngrok en un hilo
    def ngrok_thread_func():
        ngrok_service_instance_holder["instance"] = start_ngrok_service(port, endpoints, times)
    ngrok_thread = threading.Thread(target=ngrok_thread_func)
    ngrok_thread.start()
    ngrok_thread.join()
    endpoints["FastAPI"] = f"http://0.0.0.0:{port}/webhook"

    print_summary(endpoints, times, t_total_start)

    try:
        start_fastapi_service(times)
    except KeyboardInterrupt:
        print("\n\033[93mDeteniendo servicios...\033[0m")
        if ngrok_service_instance_holder.get("instance"):
            ngrok_service_instance_holder["instance"].stop()
        print("\033[92mMessenger Bridge detenido correctamente.\033[0m")

if __name__ == "__main__":
    main()
