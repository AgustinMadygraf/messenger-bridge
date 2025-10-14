"""
Path: src/interface_adapter/gateways/agent_gateway.py
"""

import requests

class AgentGateway:
    " Interfaz para comunicarse con un modelo Rasa."
    def __init__(self, agent_bot_url: str):
        self.agent_bot_url = agent_bot_url

    def get_response(self, message_or_text) -> str:
        """
        Envía el mensaje del usuario a Rasa y obtiene la respuesta.
        :param message_or_text: Message o str, mensaje o texto directo.
        :return: str, respuesta generada por Rasa.
        """
        if isinstance(message_or_text, str):
            payload = {"sender": "user", "message": message_or_text}
        else:  # Es un objeto Message u objeto similar
            payload = {"sender": "user", "message": message_or_text.body}
            if hasattr(message_or_text, 'media_url') and message_or_text.media_url:
                payload["media_url"] = message_or_text.media_url
                payload["media_type"] = message_or_text.media_type

        print(f" Enviando payload a Rasa: {payload}")  # Depuración
        try:
            response = requests.post(self.agent_bot_url, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            print(f" Respuesta recibida: {data}")  # Depuración
            # Rasa puede devolver una lista de mensajes, concatenamos los textos
            return " ".join([msg.get("text", "") for msg in data if "text" in msg])
        except requests.exceptions.RequestException as e:
            print(f" Error al comunicarse con Rasa: {e}")  # Depuración
            return f"[Error al comunicarse con Rasa: {e}]"
