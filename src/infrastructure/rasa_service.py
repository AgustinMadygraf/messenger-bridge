"""
Path: src/infrastructure/rasa_service.py
"""

from src.interface_adapter.gateways.rasa_gateway import RasaGateway

class RasaService:
    """
    Servicio que abstrae la comunicación con Rasa usando el gateway.
    """
    def __init__(self, rasa_url: str):
        self.gateway = RasaGateway(rasa_url)

    def get_response(self, prompt: str) -> str:
        """
        Obtiene una respuesta de Rasa para el prompt dado.
        :param prompt: str, mensaje del usuario.
        :return: str, respuesta generada por Rasa.
        """
        return self.gateway.get_response(prompt)
