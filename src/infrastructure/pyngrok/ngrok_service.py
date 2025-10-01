"""
Path: src/infrastructure/pyngrok/ngrok_service.py

Servicio orientado a objetos para gestionar el túnel ngrok y obtener la URL pública.
"""

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
            self.logger.info("ngrok tunnel iniciado: %s", self.public_url)
            return self.public_url
        except PyngrokNgrokError as e:
            self.logger.error("Error al iniciar ngrok: %s", e)
            print(f"Error al iniciar ngrok: {e}")
            self.public_url = None
            return None

    def stop(self):
        " Detiene todos los túneles ngrok activos."
        self.logger.info("Deteniendo todos los túneles ngrok...")
        ngrok.kill()
