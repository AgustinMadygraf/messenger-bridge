"""
Path: src/interface_adapter/gateways/agent_gateway.py
"""

import requests

class AgentGateway:
    " Interfaz para comunicarse con un modelo Rasa."
    def __init__(self, agent_bot_url: str):
        self.agent_bot_url = agent_bot_url

    def get_response(self, prompt: str) -> str:
        """
        Envía el mensaje del usuario a Rasa y obtiene la respuesta.
        :param prompt: str, mensaje del usuario.
        :return: str, respuesta generada por Rasa.
        """
        payload = {"sender": "user", "message": prompt}
        print(f" Enviando prompt a Rasa: {prompt}")  # Depuración
        try:
            response = requests.post(self.agent_bot_url, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()
            print(f" Respuesta recibida: {data}")  # Depuración
            # Rasa puede devolver una lista de mensajes, concatenamos los textos
            return " ".join([msg.get("text", "") for msg in data if "text" in msg])
        except requests.exceptions.RequestException as e:
            print(f" Error al comunicarse con Rasa: {e}")  # Depuración
            return f"[Error al comunicarse con Rasa: {e}]"
