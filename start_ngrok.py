"""
Path: start_ngrok.py
"""

from src.infrastructure.pyngrok.ngrok_service import NgrokService

if __name__ == "__main__":
    ngrok_service = NgrokService(port=5000)
    try:
        public_url = ngrok_service.start()
        if public_url:
            print(f"Túnel ngrok iniciado: {public_url}")
            print("Presiona Ctrl+C para detener el túnel.")
            import time
            while True:
                time.sleep(1)
        else:
            print("No se pudo iniciar el túnel ngrok.")
    except KeyboardInterrupt:
        print("\nDeteniendo túnel ngrok...")
        ngrok_service.stop()
        print("Túnel ngrok detenido.")
