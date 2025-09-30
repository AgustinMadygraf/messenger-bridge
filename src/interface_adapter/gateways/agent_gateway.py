"""
Path: src/interface_adapter/gateways/agent_gateway.py
"""

import requests

class AgentGateway:
    " Interfaz para comunicarse con un modelo Rasa."
    def __init__(self, rasa_url: str):
        self.rasa_url = rasa_url

    def get_response(self, prompt: str) -> str:
        """
        Envía el mensaje del usuario a Rasa y obtiene la respuesta.
        :param prompt: str, mensaje del usuario.
        :return: str, respuesta generada por Rasa.
        """
        payload = {"sender": "user", "message": prompt}
        print(f" Enviando prompt a Rasa: {prompt}")  # Depuración
        try:
            response = requests.post(self.rasa_url, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()
            print(f" Respuesta recibida: {data}")  # Depuración
            # Rasa puede devolver una lista de mensajes, concatenamos los textos
            return " ".join([msg.get("text", "") for msg in data if "text" in msg])
        except requests.exceptions.RequestException as e:
            print(f" Error al comunicarse con Rasa: {e}")  # Depuración
            return f"[Error al comunicarse con Rasa: {e}]"
