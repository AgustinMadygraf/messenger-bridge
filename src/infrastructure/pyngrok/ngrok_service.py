"""
Path: src/infrastructure/pyngrok/ngrok_service.py

Servicio orientado a objetos para gestionar el túnel ngrok y obtener la URL pública.
"""

import os
import sys
from pyngrok import ngrok

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
        temp_stdout = open(os.devnull, 'w', encoding='utf-8')
        temp_stderr = open(os.devnull, 'w', encoding='utf-8')
        sys.stdout = temp_stdout
        sys.stderr = temp_stderr

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
        finally:
            # Restore stdout/stderr before any logging
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            temp_stdout.close()
            temp_stderr.close()

        self.logger.info("ngrok tunnel iniciado: %s", self.public_url)
        return self.public_url
    def stop(self):
        "Detiene todos los túneles ngrok activos."
        self.logger.info("Deteniendo todos los túneles ngrok...")
        # Capture stdout/stderr temporarily
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        temp_stdout = open(os.devnull, 'w', encoding='utf-8')
        temp_stderr = open(os.devnull, 'w', encoding='utf-8')
        sys.stdout = temp_stdout
        sys.stderr = temp_stderr

        ngrok.kill()

        # Restore stdout/stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        temp_stdout.close()
        temp_stderr.close()
