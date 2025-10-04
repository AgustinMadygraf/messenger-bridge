"""
Path: src/infrastructure/pyngrok/ngrok_service.py

Servicio orientado a objetos para gestionar el túnel ngrok y obtener la URL pública.
"""

import os
import sys
from pyngrok import ngrok
from pyngrok.exception import PyngrokNgrokError

from src.shared.config import get_config
from src.shared.logger import get_logger

class NgrokService:
    "Servicio para gestionar el túnel ngrok."
    def __init__(self, port: int = 8443):
        self.logger = get_logger("ngrok-service")
        self.config = get_config()
        self.port = port
        self.tunnel = None
        self.public_url = None

    def start(self):
        """
        Inicia un túnel ngrok en el puerto especificado.
        Si NGROK_DOMAIN está definido en la configuración, lo usa como dominio reservado.
        Devuelve la URL pública o None si falla.
        """
        # Capture stdout/stderr temporarily to suppress ngrok output
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w', encoding='utf-8')
        sys.stderr = open(os.devnull, 'w', encoding='utf-8')

        ngrok_domain = self.config.get("NGROK_DOMAIN")
        try:
            if ngrok_domain:
                self.logger.info("Iniciando ngrok con dominio reservado: %s", ngrok_domain)
                self.tunnel = ngrok.connect(
                    addr=self.port,
                    bind_tls=True,
                    domain=ngrok_domain
                )
            else:
                self.logger.info("Iniciando ngrok con dominio aleatorio")
                self.tunnel = ngrok.connect(addr=self.port, bind_tls=True)

            self.public_url = self.tunnel.public_url

            # Restore stdout/stderr
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = original_stdout
            sys.stderr = original_stderr

            self.logger.info("ngrok tunnel iniciado: %s", self.public_url)
            return self.public_url
        except PyngrokNgrokError as e:
            # Restore stdout/stderr
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = original_stdout
            sys.stderr = original_stderr

            # Extract the most useful part of the error message
            error_message = str(e)
            if "ERR_NGROK_108" in error_message:
                simplified_error = "Error: Ya existe una sesión de ngrok activa. Ciérrala antes de continuar."
            elif "ERR_NGROK_105" in error_message:
                simplified_error = "Error: El dominio especificado no está disponible o no pertenece a tu cuenta."
            else:
                simplified_error = f"Error de ngrok: {str(e).split('.', maxsplit=1)[0]}"

            self.logger.error(simplified_error)
            print(f"\n[ERROR] {simplified_error}")

            # Provide suggestions
            if "simultaneous ngrok agent sessions" in error_message:
                print("\nSugerencias:")
                print("1. Cierra otras sesiones de ngrok que estén en ejecución")
                print("2. Verifica en https://dashboard.ngrok.com/tunnels si hay túneles activos")
                print("3. Ejecuta 'ngrok authtoken <tu-token>' si has cambiado de cuenta")

            self.public_url = None
            return None

    def stop(self):
        " Detiene todos los túneles ngrok activos."
        self.logger.info("Deteniendo todos los túneles ngrok...")
        # Capture stdout/stderr temporarily
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w', encoding='utf-8')
        sys.stderr = open(os.devnull, 'w', encoding='utf-8')

        ngrok.kill()

        # Restore stdout/stderr
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = original_stdout
        sys.stderr = original_stderr
