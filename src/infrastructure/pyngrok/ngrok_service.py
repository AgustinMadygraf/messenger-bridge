"""
Path: src/infrastructure/pyngrok/ngrok_service.py

Servicio para gestionar el túnel ngrok y obtener la URL pública.
"""

from pyngrok import ngrok
from pyngrok.exception import PyngrokNgrokError

from src.shared.config import get_config
from src.shared.logger import get_logger

logger = get_logger("ngrok-service")
config = get_config()

def start_ngrok_tunnel(port: int = 5000):
    """
    Inicia un túnel ngrok en el puerto especificado.
    Si NGROK_DOMAIN está definido en la configuración, lo usa como dominio reservado.
    Devuelve la URL pública.
    """
    ngrok_domain = config.get("NGROK_DOMAIN")
    try:
        if ngrok_domain:
            logger.info("Iniciando ngrok con dominio reservado: %s", ngrok_domain)
            public_url = ngrok.connect(
                addr=port,
                bind_tls=True,
                domain=ngrok_domain
            ).public_url
        else:
            logger.info("Iniciando ngrok con dominio aleatorio")
            public_url = ngrok.connect(addr=port, bind_tls=True).public_url

        logger.info("ngrok tunnel iniciado: %s", public_url)
    except PyngrokNgrokError as e:
        logger.error("Error al iniciar ngrok: %s", e)
        print(f"Error al iniciar ngrok: {e}")
        return None

def stop_ngrok_tunnels():
    "Detiene todos los túneles ngrok activos."
    logger.info("Deteniendo todos los túneles ngrok...")
    ngrok.kill()
