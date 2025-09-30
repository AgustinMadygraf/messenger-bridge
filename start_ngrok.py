"""
Path: start_ngrok.py
"""

from src.infrastructure.pyngrok.ngrok_service import start_ngrok_tunnel, stop_ngrok_tunnels

if __name__ == "__main__":
    try:
        public_url = start_ngrok_tunnel(port=5000)
        print(f"Túnel ngrok iniciado: {public_url}")
        print("Presiona Ctrl+C para detener el túnel.")
        # Mantener el script corriendo hasta interrupción manual
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeteniendo túnel ngrok...")
        stop_ngrok_tunnels()
        print("Túnel ngrok detenido.")
